#!/usr/bin/env python3
"""Empacota um pacote Python em um único arquivo .py.

Mantém comentários, nomes de variáveis e imports externos.
Imports locais são resolvidos recursivamente e removidos do código gerado.
"""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Set, Tuple


@dataclass(frozen=True)
class ModuleRef:
    file_path: Path
    module_name: str


def find_source_path(source: str) -> Path:
    source_path = Path(source)
    if source_path.exists():
        return source_path.resolve()

    source_path = Path.cwd() / source
    if source_path.exists():
        return source_path.resolve()

    parts = source.split('.')
    source_path = Path.cwd().joinpath(*parts)
    if source_path.exists():
        return source_path.resolve()

    source_path = Path.cwd().joinpath(*parts).with_suffix('.py')
    if source_path.exists():
        return source_path.resolve()

    raise FileNotFoundError(f"Pacote ou módulo não encontrado: {source}")


def resolve_module_name(file_path: Path, package_root: Path, root_package_name: str) -> str:
    relative = file_path.relative_to(package_root)
    parts = list(relative.with_suffix('').parts)
    if parts and parts[-1] == '__init__':
        parts = parts[:-1]
    return '.'.join([root_package_name] + parts) if parts else root_package_name


def resolve_module_path(module_name: str, package_root: Path, root_package_name: str) -> Optional[ModuleRef]:
    if not module_name:
        return None

    parts = module_name.split('.')
    if parts[0] == root_package_name:
        parts = parts[1:]

    if not parts:
        init_path = package_root / '__init__.py'
        if init_path.exists():
            return ModuleRef(init_path, root_package_name)
        return None

    candidate = package_root.joinpath(*parts)
    if candidate.is_file() and candidate.suffix == '.py':
        return ModuleRef(candidate, resolve_module_name(candidate, package_root, root_package_name))

    if candidate.is_dir() and (candidate / '__init__.py').exists():
        init_file = candidate / '__init__.py'
        return ModuleRef(init_file, resolve_module_name(init_file, package_root, root_package_name))

    if candidate.with_suffix('.py').exists():
        target = candidate.with_suffix('.py')
        return ModuleRef(target, resolve_module_name(target, package_root, root_package_name))

    return None


def absolute_local_name(
    current_module_name: str,
    level: int,
    module_name: Optional[str],
    root_package_name: str,
) -> str:
    parts = current_module_name.split('.')
    if parts and parts[0] == root_package_name:
        parts = parts[1:]

    if level > 0:
        if level > len(parts) + 1:
            return ''
        base_parts = parts[:-level]
    else:
        base_parts = []

    module_parts = module_name.split('.') if module_name else []
    full_parts = base_parts + module_parts
    return '.'.join([root_package_name] + full_parts) if full_parts else root_package_name


def merge_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    if not ranges:
        return []
    ranges = sorted(ranges, key=lambda item: (item[0], item[1]))
    merged: List[Tuple[int, int]] = []
    start, end = ranges[0]
    for current_start, current_end in ranges[1:]:
        if current_start <= end + 1:
            end = max(end, current_end)
        else:
            merged.append((start, end))
            start, end = current_start, current_end
    merged.append((start, end))
    return merged


def remove_lines_by_ranges(lines: List[str], ranges: List[Tuple[int, int]]) -> List[str]:
    cleaned: List[str] = []
    for start, end in merge_ranges(ranges):
        cleaned.extend(lines[:start])
        cleaned = cleaned[:start] if cleaned else []
        cleaned.extend(lines[end + 1:])
    # The above logic is wrong; use iterative removal.
    cleaned = []
    current = 0
    for start, end in merge_ranges(ranges):
        cleaned.extend(lines[current:start])
        current = end + 1
    cleaned.extend(lines[current:])
    return cleaned


def analyze_module(
    module_path: Path,
    module_name: str,
    package_root: Path,
    root_package_name: str,
) -> Tuple[str, List[ModuleRef]]:
    source = module_path.read_text(encoding='utf-8')
    tree = ast.parse(source)
    lines = source.splitlines()
    removed_ranges: List[Tuple[int, int]] = []
    local_deps: List[ModuleRef] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            local_targets: List[ModuleRef] = []
            for alias in node.names:
                local_module = resolve_module_path(alias.name, package_root, root_package_name)
                if local_module is not None:
                    local_targets.append(local_module)
            if local_targets:
                removed_ranges.append((node.lineno - 1, getattr(node, 'end_lineno', node.lineno) - 1))
                for target in local_targets:
                    if target not in local_deps:
                        local_deps.append(target)

        elif isinstance(node, ast.ImportFrom):
            abs_name = absolute_local_name(
                module_name,
                node.level,
                node.module,
                root_package_name,
            )
            local_targets: List[ModuleRef] = []
            resolved = resolve_module_path(abs_name, package_root, root_package_name)
            if resolved is not None:
                local_targets.append(resolved)
                if resolved.file_path.name == '__init__.py':
                    for alias in node.names:
                        if alias.name == '*':
                            continue
                        alias_name = f"{abs_name}.{alias.name}"
                        alias_target = resolve_module_path(alias_name, package_root, root_package_name)
                        if alias_target is not None and alias_target not in local_targets:
                            local_targets.append(alias_target)

            elif node.module:
                for alias in node.names:
                    if alias.name == '*':
                        continue
                    alias_name = absolute_local_name(
                        module_name,
                        node.level,
                        f"{node.module}.{alias.name}",
                        root_package_name,
                    )
                    alias_target = resolve_module_path(alias_name, package_root, root_package_name)
                    if alias_target is not None:
                        local_targets.append(alias_target)

            if local_targets:
                removed_ranges.append((node.lineno - 1, getattr(node, 'end_lineno', node.lineno) - 1))
                for target in local_targets:
                    if target not in local_deps:
                        local_deps.append(target)

    cleaned_lines = remove_lines_by_ranges(lines, removed_ranges)
    cleaned_source = '\n'.join(cleaned_lines).rstrip() + '\n'
    return cleaned_source, local_deps


def find_package_root_and_name(source_path: Path) -> Tuple[Path, str, Path]:
    if source_path.is_dir():
        package_root = source_path
        root_name = source_path.name
        entry_path = package_root / '__main__.py'
        if entry_path.exists():
            return package_root, root_name, entry_path
        init_path = package_root / '__init__.py'
        if init_path.exists():
            return package_root, root_name, init_path
        return package_root, root_name, package_root

    if source_path.is_file() and source_path.suffix == '.py':
        package_root = source_path.parent
        root_name = package_root.name
        return package_root, root_name, source_path

    raise FileNotFoundError(f"Fonte não encontrada: {source_path}")


def collect_ordered_modules(entry_path: Path, package_root: Path, root_name: str) -> List[Tuple[ModuleRef, str]]:
    entry_module_name = resolve_module_name(entry_path, package_root, root_name)
    entry_ref = ModuleRef(entry_path, entry_module_name)
    ordered: List[Tuple[ModuleRef, str]] = []
    visited: Set[Path] = set()

    def visit(module_ref: ModuleRef) -> None:
        if module_ref.file_path in visited:
            return
        visited.add(module_ref.file_path)
        cleaned_source, deps = analyze_module(
            module_ref.file_path,
            module_ref.module_name,
            package_root,
            root_name,
        )
        for dep in deps:
            visit(dep)
        ordered.append((module_ref, cleaned_source))

    visit(entry_ref)
    return ordered


def build_flat_file(modules: List[Tuple[ModuleRef, str]], package_root: Path) -> str:
    lines: List[str] = ["from __future__ import annotations", ""]
    for module_ref, source in modules:
        rel_path = module_ref.file_path.relative_to(package_root)
        lines.append(f"# --- Begin {module_ref.module_name} ({rel_path}) ---")
        lines.append(source.rstrip())
        lines.append("")
    return '\n'.join(lines).rstrip() + '\n'


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Empacota um pacote Python em um único arquivo .py.',
    )
    parser.add_argument('source', help='Pacote ou módulo Python (ex: app ou app/__main__.py)')
    parser.add_argument('output', help='Arquivo de saída .py (ex: programa.py)')
    args = parser.parse_args()

    source_path = find_source_path(args.source)
    package_root, root_name, entry_path = find_package_root_and_name(source_path)
    if entry_path is package_root:
        raise ValueError('Não foi possível determinar um módulo de entrada no pacote informado.')

    modules = collect_ordered_modules(entry_path, package_root, root_name)
    code = build_flat_file(modules, package_root)
    Path(args.output).write_text(code, encoding='utf-8')
    print(f'Arquivo gerado em: {args.output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
