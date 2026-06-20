# Implementation Assignment - Algorithm Design and Analysis - 2026-1 - Master's Program in Computer Science

Implementation assignment for the Algorithm Design and Analysis course within the Master's Program in Computer Science at PUC Minas.

## Assignment Brief

Pontifical Catholic University of Minas Gerais

Graduate Program in Computer Science

Course: Algorithm Design and Analysis

Prof. Alexei Machado

### Implementation Assignment

Value: 40 points

Date: June 23, 2026, at 7:00 PM via Canvas.

Individual assignment

#### Description

The problem of matching (alignment, warping) between two time series consists of establishing a similarity (or distance) measure between time-ordered sequences—possibly of different lengths—that are subject to noise, scale variations, temporal shifts, and non-linear distortions. This problem is central to various applications, such as biomedical signal analysis, speech and audio recognition, industrial monitoring, and finance.

Formally, given two time series X = (x1, x2, ..., xn) and Y = (y1, y2, ..., ym), the objective is to find an alignment or a matching function u(xi)=yj that associates each element of X with an element of Y, minimizing a cost measure between the elements of the two series while respecting certain temporal constraints, such as monotonicity and continuity. Thus, if an element xi is associated with an element yj, any xk (where k > i) must be associated with some yl (where l ≥ j). Fig. 1 shows an example of mapping X to Y, and Fig. 2 shows a schematic of the alignment result in matrix form.

<img src=".github/images/fig1.png" alt="Figure 1. Example of mapping series X (blue) to series Y (red). This figure shows a 3D plot relating one time series to another.">

Figure 1. Example of mapping series X (blue) to series Y (red).

<img src=".github/images/fig2.png" alt="Figure 2. Example of mapping series A (blue) to series B (green). This figure shows a 2D grid plot relating one time series to another.">

Figure 2. Example of mapping series A (blue) to series B (green).

A significant challenge is that similar events may occur at different paces in the two series. For example, two electrocardiogram signals might represent the same physiological phenomenon but with different heart rates, making simple point-to-point comparisons unfeasible. Therefore, during alignment, an interval in X may undergo compression or expansion if mapped to an interval of shorter or longer length, respectively.

It is easy to see that a brute-force solution to the time series matching problem would have exponential complexity, as each of the n elements in X could be mapped to any of the m elements in Y, resulting in O(nm) complexity. However, the dynamic programming design technique can reduce this complexity to a polynomial function while requiring minimal auxiliary memory.

In this project, you will implement efficient dynamic programming-based solutions for the time series alignment problem and analyze the behavior of various datasets when subjected to these solutions. The algorithm used as a baseline for experimental comparison will be Dynamic Time Warping (DTW) (Sakoe & Chiba, 1978; Berndt & Clifford, 1994), from which variations such as the following have been proposed:

1.  Continuous Dynamic Time Warping (Munich & Perona, 1999; Buchin et al. 2022).

2.  Derivative Dynamic Time Warping (Keogh & Pazzani, 2001).

3.  Longest Common Subsequence (Vlachos et al. 2002).

4.  Edit Distance on Real Sequence (Chen et al. 2005).

5.  Time Warp Edit Distance (Marteau, 2009).

6.  Soft-DTW (Cuturi & Blondel, 2017).

7.  ShapeDTW (Zhao & Itti, 2018).

8.  Amerced Dynamic Time Warping (Herrmann & Webb, 2023).

#### Implementation

1.  Develop a graphical interface for the project to display two series side-by-side and the mapping between them, similar to the example in Fig. 1. This will serve to evaluate whether the algorithms are performing the mapping correctly. Also, provide the alignment matrix similar to Fig. 2.

2.  Implement the basic DTW algorithm, including a search window option (Constrained DTW) (Sakoe & Chiba, 1978; Berndt & Clifford, 1994).

3.  Implement the competing algorithms assigned to you.
4.  Conduct experiments using the datasets assigned to you from the UCR Time Series Archive (Dau et al. 2019) (https://www.cs.ucr.edu/%7Eeamonn/time_series_data_2018/). Each dataset consists of a description file (readme), a training file, and a test file in TSV format. Each line of the file represents a series, with the first position indicating the class number and the remaining positions containing the series values. Consult the documentation on the website for further details and plot examples.

5. The results obtained with the implemented algorithms should serve as the basis for a classifier of your choice. The Nearest Neighbor (1-NN) method often yields very good results, but other classifiers may be tested. Use the training set from the datasets to tune the classifier if necessary, but the error rate must be calculated using the test set. For example, you can align each series X from the test set with the series Y from the training set and select the one that produced the lowest alignment cost. Then, simply check if the class of X matches that of series Y. Report the accuracy rate for each dataset and determine which algorithm achieved the highest accuracy.

6. Analyze the behavior of the datasets in relation to the algorithms to identify groups of datasets that exhibit high result correlation. Calculate the Spearman correlation matrix among the datasets based on the accuracy values ​​obtained by the 5 algorithms (DTW plus the randomly selected ones). Plot the matrix as a heatmap. This matrix will represent the edge weights of a complete graph, where the vertices are the datasets.

7. Based on the resulting graph, implement an efficient solution for the maximum clique problem; this will identify the largest group of datasets with high inter-element correlation. The correlation threshold value should be a parameter of the method. Once the maximum clique is found, remove the corresponding vertices and apply the method to the remaining ones to find the next maximum clique, and so on, until all vertices have been grouped.

8. Present the time complexity analysis of the algorithms and measure the average time required to run the experiments (calculate the mean and standard deviation). Compare and discuss the values. Do not forget to specify the hardware configuration and software used.

9. Present the complexity analysis regarding the algorithms' memory usage.

| Student | Algorithms | Datasets |
| ------| -----------|----------|
| Henrique Mendonça Castelar Campos | DTW+1+2+3+6 | 97 to 128 |

#### Documentation

Document the solutions and tests in a technical report (LaTeX and PDF formats, maximum 15 pages) following the SBC single-column standard, containing the following sections:

a. Introduction: Describe the problem and the objective of the assignment.

b. Proposed solution: Describe the algorithms used to solve the problem using pseudocode.

c. Implementation: Describe the datasets and details of the implemented programs, particularly those used to improve the solution's efficiency.

d. Test report: Describe the tests performed and their results, showing the resulting alignment for specific examples.

e. Conclusion: Discuss the results obtained, comparing the solutions in terms of time and memory complexity order and measured execution time.

f. Bibliography following the ABNT standard.

General considerations and evaluation criteria

1.  The assignment must be completed individually; the use of AI-based code or documentation generators is prohibited. However, implementation examples may be consulted in repositories and must be properly referenced in the documentation.

2.  The code must be written in Python, Java, or C++ and contained in a single file.

3.  The submissions (source code and report with LaTeX source files and final PDF) must be uploaded as a ZIP archive with a maximum size of 10 MB. Do not include the datasets in the archive. Source files must be located in the archive's root directory and must include the names of all group members at the beginning of the code. The presentation will be based on the code submitted via Canvas.

4.  Evaluation will be based on the following criteria:

•  Correctness, robustness, and efficiency of the programs regarding processing time and memory usage

•  Compliance with specifications

•  Clarity and coding style (comments, indentation, choice of identifier names, parameterization)

•  Report

#### References

Sakoe, H., & Chiba, S. (1978). Dynamic programming algorithm optimization for spoken word recognition. IEEE Transactions on Acoustics, Speech, and Signal Processing, 26(1), 43–49.

Berndt, D. J., & Clifford, J. (1994). Using dynamic time warping to find patterns in time series. AAAI Workshop on Knowledge Discovery in Databases.

Munich, M. E., & Perona, P. (1999, September). Continuous dynamic time warping for translation-invariant curve alignment with applications to signature verification. In Proceedings of the Seventh IEEE International Conference on Computer Vision (Vol. 1, pp. 108-115). IEEE.

Keogh, E., & Pazzani, M. (2001). Derivative Dynamic Time Warping. In Proceedings of the 1st SIAM International Conference on Data Mining (SDM).

Vlachos, M., Kollios, G., & Gunopulos, D. (2002). Discovering similar multidimensional trajectories. Proceedings of the 18th International Conference on Data Engineering (ICDE).

Chen, L., Özsu, M. T., & Oria, V. (2005). Robust and fast similarity search for moving object trajectories. Proceedings of the ACM SIGMOD International Conference on Management of Data.

Keogh, E., & Ratanamahatana, C. A. (2005). Exact indexing of dynamic time warping. Knowledge and information systems, 7(3), 358-386.

Marteau, P.-F. (2009). Time Warp Edit Distance with stiffness adjustment for time series matching. IEEE Transactions on Pattern Analysis and Machine Intelligence, 31(2), 306–318.

Zhao, J., & Itti, L. (2018). shapedtw: Shape dynamic time warping. Pattern Recognition, 74, 171-184.

Dau, H. A., Bagnall, A., Kamgar, K., Yeh, C. C. M., Zhu, Y., Gharghabi, S., ... & Keogh, E. (2019). The UCR time series archive. IEEE/CAA Journal of Automatica Sinica, 6(6), 1293-1305.

Cuturi, M., & Blondel, M. (2017). Soft-DTW: a differentiable loss function for time-series. Proceedings of the 34th International Conference on Machine Learning (ICML).

Buchin, K., Nusser, A., & Wong, S. (2022). Computing continuous dynamic time warping of time series in polynomial time. arXiv preprint arXiv:2203.04531.

Herrmann, Matthieu; Webb, Geoffrey I. (2023). "Amercing: An intuitive and effective constraint for dynamic time warping". Pattern Recognition. 137 109333.