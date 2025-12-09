# 泛函分析定理整理

## 第一章 距离空间

### §1.3 距离空间的完备性

#### Thm 1. (闭球套定理)
设 $(X,d)$ 是完备的距离空间，$\overline{S_n} = S_n(x_n, r_n)$ 是 $X$ 中一个闭球套 (列)，满足条件：
(1) $\overline{S_n} \supset \overline{S_{n+1}}$
(2) $r_n \to 0$
则 $\exists ! x_0 \in X$, 使 $\cap_{n=1}^\infty \overline{S_n} = \{x_0\}$.

#### Thm 2. (完备性的等价条件)
设 $X$ 是距离空间，若 $X$ 中任意满足 Thm 1 的闭球套的交集是 $X$ 中唯一的一点，则 $X$ 完备。

### §1.4 压缩映射原理及应用

#### Thm 1. (Banach 压缩映射原理)
设 $(X,d)$ 是完备的距离空间，$T$ 是 $X$ 到自身的一个压缩映射，满足条件：$\exists \alpha (0 \le \alpha < 1)$ s.t. $\forall x, y \in X, d(Tx, Ty) \le \alpha d(x,y)$.
则 $\exists ! x^* \in X$ s.t. $Tx^* = x^*$.

#### Thm 2. (压缩映射原理的推广)
设 $X$ 是完备距离空间，$T$ 是 $X$ 到自身的映射。若存在正整数 $n_0$，使 $T^{n_0}$ 是 $X$ 到自身的压缩映射，则存在唯一的 $x^* \in X$ 使 $Tx^* = x^*$.

---

## 第二章 拓扑空间

### §2.1 拓扑空间基本概念

#### Prop 1. (连续映射的等价条件)
若 $f$ 是拓扑空间 $X \to Y$ 的一个映射，则 $f$ 连续 $\Leftrightarrow Y$ 中开集的原像也是开集。

#### Cor 1. (连续映射的等价条件)
连续映射 $\Leftrightarrow$ 闭集的原像也是闭集。

#### Cor 2. (同胚映射的性质)
同胚映射下开集的像是开集，闭集的像是闭集。

#### Prop. (Hausdorff 空间的性质)
Hausdorff 空间中的单点集是闭集。

### §2.2 拓扑空间中的紧集与紧空间

#### 性质 1. (紧空间的闭子集)
紧空间的闭子集是紧集。

#### 性质 2. (Hausdorff 空间上的紧子集)
Hausdorff 空间上的紧子集是闭集。

#### Cor. (紧集的闭子集)
紧集的闭子集还是紧集。

#### 性质 3. ($\R^n$ 中紧集的等价条件)
$\R^n$ 中紧集 $\Leftrightarrow$ 有界闭集。

#### 性质 4. (连续映射下紧集的像)
连续映射下，紧集的像仍是紧集。

#### 性质 5. (Hausdorff 空间上连续函数的最值)
Hausdorff 空间上连续函数在紧集上有最值。

---

## 第三章 赋范线性空间

### §3.2 赋范线性空间

#### 性质 1. (赋范空间基本不等式)
$\forall x, y \in X, |\|x\| - \|y\|| \le \|x-y\|$

#### 性质 2. (范数的连续性)
赋范空间中范数 $\|\cdot\|$ 可看成 $X$ 的非负实函数，则该函数在收敛点处连续，即若 $x_n \to x_0$，则 $\|x_n\| \to \|x_0\|$.

#### Cor. (收敛的线性组合)
若赋范空间 $X$ 中， $x_n \in X, \alpha_n \in \K$ ($X$ 相关的数域)，当 $x_n \to x_0, \alpha_n \to \alpha$，则 $\alpha_n x_n \to \alpha x_0$.

#### 性质 3. (Banach 空间的等价条件)
设 $X$ 是赋范空间，则 $X$ 是 Banach 空间 $\Leftrightarrow$ 对 $X$ 中任意 $\sum \|x_n\|$ 收敛的级数都有 $\sum x_n$ 收敛。

### §3.2 $L^p(E)$ 空间的完备性

#### Thm 1. ($L^p(E)$ 是 Banach 空间)
$L^p(E)$ 是 Banach 空间。

#### Thm 2. ($\ell^p$ 是 Banach 空间)
$\ell^p$ 是 Banach 空间。

### §3.3 范数的等价性与赋范空间的完备化

#### 性质 2. (范数等价的完备性)
设 $(X, \|\cdot\|_1)$ 与 $(X, \|\cdot\|_2)$ 是两个赋范线性空间，若 $\|\cdot\|_1 \sim \|\cdot\|_2$，则 $(X, \|\cdot\|_1)$ 是 Banach 空间 $\Leftrightarrow (X, \|\cdot\|_2)$ 是 Banach 空间。

#### Thm. (距离空间的完备化)
任意不完备的距离空间均存在唯一完备化空间。

#### Thm. (赋范空间的完备化)
任意赋范空间都可以扩充为 Banach 空间。

### §3.4 有限维赋范线性空间的性质

#### Thm. (Hamel 基的存在性)
任何非平凡赋范线性空间都存在 Hamel 基。

#### Prop 1. (有限维空间中范数的等价性)
任意有限维赋范空间中定义所有不同范数都等价。

#### Prop 2. (有限维空间与 $\R^n$ 的同构)
任意 $n$ 维赋范空间与欧氏空间 $\R^n$ 同构且同胚。

#### Cor 1. (有限维空间的同构映射)
对任意 $n$ 维赋范空间 $X$，$\forall \varepsilon > 0, \exists \R^n \to X$ 的同构映射满足 $\forall \tilde{x} \in \R^n$，都有 $\|T \tilde{x}\|_1 \le \alpha \|\tilde{x}\|$，其中 $\|\cdot\|_1$ 为 $X$ 的范数，$\|\cdot\|$ 为 $\R^n$ 的范数。

#### Cor 2. (有限维空间之间的同构)
设 $(X, \|\cdot\|_1)$ 和 $(Y, \|\cdot\|_2)$ 是两个同数域上的 $n$ 维赋范空间，则 $\exists \alpha, \beta > 0, X \to Y$ 的同构且同胚映射 $T$, 使 $\forall x \in X, y \in Y$ 有：
$\|T x\|_2 \le \alpha \|x\|_1, \|T^{-1} y\|_1 \le \beta \|y\|_2$.

#### Cor 3. (有限维空间是 Banach 空间)
任意 $n$ 维赋范线性空间 $X$ 都是 Banach 空间 (与 $\R^n$ 结构相同)。

#### Prop 3. (有限维空间的等价条件)
$X$ 是有限维赋范线性空间 $\Leftrightarrow X$ 中任意有界闭集都是列紧集。

#### Prop 4. (无限维空间的等价条件)
$X$ 是无限维赋范线性空间 $\Leftrightarrow X$ 中存在有界闭集不是列紧集。

---

## 第四章 线性算子与线性泛函

### §4.2 有界线性算子空间

#### Thm 1. (有界线性算子空间的完备性)
设 $B(X \to X_1)$ 是一个有界算子空间，若 $X_1$ 是 Banach 空间，则 $B$ 是 Banach 空间。

#### Cor 1. (算子空间的完备性)
设 $X_1$ 是 Banach 空间，则 $B(X \to X)$ 也是 Banach 空间。

#### Cor 2. (共轭空间的完备性)
设 $X$ 是赋范空间，则 $B(X \to \R)$ 也是 Banach 空间。

### §4.3 算子序列的收敛性

#### Prop. (强收敛与弱收敛的关系)
(1) 强收敛 $\Rightarrow$ 弱收敛
(2) 有限维赋范空间中强收敛 $\Leftrightarrow$ 弱收敛。

#### Prop. (一致收敛与强收敛)
若 $\{T_n\} \subset B(X \to X_1)$，且 $\{T_n\}$ 在 $X$ 上一致收敛至 $T$，则 $\{T_n\}$ 在 $X$ 上强收敛至 $T$.

#### Prop. (算子范数收敛与一致收敛)
设 $B(X \to X_1), \{T_n\} \subset B, T \in B$，则 $\{T_n\}$ 依算子范数收敛至 $T \Leftrightarrow \{T_n\}$ 在 $X$ 的任意有界子集上一致收敛。

#### Cor. (算子范数收敛的等价条件)
(1) 设 $B(X \to X_1), \{T_n\} \subset B, T \in B$，则 $\{T_n\}$ 依范数收敛至 $T \Leftrightarrow \{T_n\}$ 在 $S_0$ 上一致收敛至 $T$.
(2) 设 $B(X \to X_1), \{T_n\} \subset B, T \in B$，若 $\{T_n\}$ 在 $X$ 上一致收敛至 $T$，则 $\{T_n\}$ 依范数收敛至 $T$.

### §4.4 Banach 空间上算子的进一步性质

#### Thm 1. (逆算子定理)
设 $X$ 和 $X_1$ 都是 Banach 空间，且 $T \in B(X \to X_1)$，若 $T$ 是 $X \to X_1$ 的一一映射算子，则 $T^{-1}$ 是 $X_1 \to X$ 的有界线性算子。

#### Lem. (范数等价性引理)
设 $(X, \|\cdot\|_1)$ 和 $(X, \|\cdot\|_2)$ 都是 Banach 空间，且 $\|\cdot\|_1$ 弱于 $\|\cdot\|_2$，则 $\|\cdot\|_1 \sim \|\cdot\|_2$.

#### Thm 2. (Banach 共鸣定理)
设 $(X, \|\cdot\|)$ 是 Banach 空间，$(X_1, \|\cdot\|)$ 是赋范空间，若对 $B(X \to X_1)$ 中一个子集族 $\{T_\alpha\} = \{T_\alpha \in B : \alpha \in I\}$ 满足 $\forall x \in X$，都有 $\sup_{\alpha \in I} \|T_\alpha x\| < \infty$，则 $\{T_\alpha\}$ 是一致有界的：$\exists M > 0, \forall \alpha \in I, \|T_\alpha\| \le M$.

#### Cor. (共鸣定理的推论)
设 $X$ 和 $X_1$ 都是 Banach 空间，$\{T_n\} \subset B(X \to X_1)$，若 $\forall x \in X, \{T_n x\}$ 收敛，则存在 $T_0 \in B(X \to X_1)$ s.t. $\lim_{n \to \infty} T_n = T_0$.

#### Thm 3. (开映射定理)
设 $X$ 和 $X_1$ 都是 Banach 空间，$T \in B(X \to X_1)$，若 $T$ 是满射，则 $T$ 是一个开映射。

### §4.5 延拓定理及某些线性泛函的表示

#### Thm 1. (Hahn-Banach 延拓定理 - 算子形式)
设 $X$ 是赋范空间，$X_1$ 是 Banach 空间，$G$ 是 $X$ 的一个稠密线性子空间，若 $T_0 \in B(G \to X_1)$，则 $T_0$ 可延拓为 $X \to X_1$ 上的有界线性算子 $T$，满足：
(1) $\forall x \in G, T x = T_0 x$
(2) $\|T\|_X = \|T_0\|_G$
(3) 延拓是唯一的。

#### Thm 2. (Hahn-Banach 延拓定理 - 泛函形式)
设 $X$ 是一个赋范线性空间，$G$ 是 $X$ 的一个线性子空间，$\forall T_0 \in B(G \to \R)$，$G$ 上任一个有界线性泛函可延拓为 $X$ 上任一个有界线性泛函 $F$，满足：
(1) $\forall x \in G, F(x) = f(x)$.
(2) $\|F\|_X = \|f\|_G$.

#### Thm 3. ($L^p[a,b]$ 上有界线性泛函的表示)
设 $f$ 是 $L^p[a,b]$ 上的有界线性泛函，存在唯一 $y(t) \in L^q[a,b]$,
使 $\forall x \in L^p[a,b], f(x) = \int_a^b y(t) x(t) dt$，且 $\|f\| = \|y\|_q$，其中 $\frac{1}{p} + \frac{1}{q} = 1$.

#### Cor. ($L^p$ 空间的共轭空间)
$L^p[a,b]^* = L^q[a,b]$.

#### Thm 4. ($\ell^p$ 上有界线性泛函的表示)
设 $f$ 是 $\ell^p$ 上的有界线性泛函，则存在唯一 $y = \{\eta_i\} \in \ell^q$,
使 $\forall x = \{\xi_i\} \in \ell^p, f(x) = \sum_{i=1}^\infty \eta_i \xi_i$, 且 $\|f\| = \|y\|_q$, 其中 $\frac{1}{p} + \frac{1}{q} = 1$.
且 $(\ell^p)^* = \ell^q$.

#### Thm 5. ($\ell^1$ 上有界线性泛函的表示)
设 $f$ 是 $\ell^1$ 上的有界线性泛函，则存在唯一 $y = \{\eta_i\} \in \ell^\infty$, 使
$\forall x = \{\xi_i\} \in \ell^1, f(x) = \sum_{i=1}^\infty \eta_i \xi_i$, 且 $\|f\| = \|y\|_1$, 其中 $\frac{1}{p} + \frac{1}{q} = 1$.

#### Cor. ($\ell^1$ 空间的共轭空间)
$(\ell^1)^* = \ell^\infty \Leftrightarrow (\ell^\infty)^* = \ell^1$.

#### Thm 6. ($C[a,b]$ 上有界线性泛函的表示)
设 $f$ 是 $C[a,b]$ 上的有界线性泛函，则存在唯一 $y \in V[a,b]$, 使
$\forall x = x(t) \in C[a,b], f(x) = \int_a^b x(t) dy(t)$, 且 $\|f\| = \|y\|_1$, 其中 $\frac{1}{p} + \frac{1}{q} = 1$. (注：此处应为 Stieltjes 积分)

---

## 第五章 Hilbert 空间

### §5.1 内积空间与 Hilbert 空间的基本性质

#### Thm. (范数诱导内积的充要条件)
设 $H$ 是赋范线性空间，则 $H$ 上的范数能诱导内积使 $(x,x) = \|x\|^2 \Leftrightarrow \|x+y\|^2 + \|x-y\|^2 = 2(\|x\|^2 + \|y\|^2)$.

### §5.2 内积空间的正交分解定理和 Riesz 表示定理

#### Thm 1. (正交分解定理 / 投影定理)
设 $H$ 是内积空间，$M \subset H$，若 $M$ 是 Hilbert 空间，则 $\forall x \in H, \exists ! x_0 \in M$ 且 $x_1 \in M^\perp$ 使 $x = x_0 + x_1$.

#### Cor 1. (正交分解的直和表示)
设 $H$ 是内积空间，$M \subset H$ 是 Hilbert 空间，则 $H = M \oplus M^\perp$.

#### Cor 2. (Hilbert 空间的正交分解)
设 $H$ 是 Hilbert 空间，$M$ 是 $H$ 的闭子集，则 $H = M \oplus M^\perp$ 且 $H$ 中元素表示唯一。

#### Thm 2. (Riesz 表示定理)
设 $H$ 是 Hilbert 空间，$f$ 是 $H$ 上的一个有界线性泛函，则存在唯一 $x_f \in H$ s.t. $f(x) = (x, x_f)$，且 $\|f\| = \|x_f\|$.

### §5.3 内积空间的正交系与正交基

#### Thm 1. (Bessel 不等式)
设 $\{e_n\}$ 是内积空间 $H$ 的一个可数标准正交系，则 $\forall x \in H$，都有 Bessel 不等式：$\sum_{i=1}^\infty |(x, e_i)|^2 \le \|x\|^2$.

#### Thm 2. (Bessel 不等式的等号成立条件)
设 $H$ 是 Hilbert 空间，$\{e_n\}$ 是 $H$ 的一个标准正交系，则 Bessel 等式成立与下列条件的等价：
(1) $x \in E$, $E$ 是 $\{e_n\}$ 的闭包；
(2) $\sum_{i=1}^\infty |(x, e_i)|^2 = \|x\|^2$;
(3) $x = \sum_{i=1}^\infty (x, e_i) e_i$.

#### Thm 3. (Schmidt 正交化方法)
设 $H$ 是内积空间，$A$ 是 $H$ 的可数子集且 $A$ 中含非零元，则存在一个可数正交系 $\{e_n\}$ s.t. $\overline{\{e_n\}} = \overline{A}$.

#### Cor 1. (标准正交系的存在性)
任意非平凡内积空间存在标准正交系。

#### Cor 2. (可数标准正交基的存在性)
可分的内积空间一定存在可数的标准正交基。

#### Lem 1. ($C[0, 2\pi]$ 的稠密性)
$C[0, 2\pi]$ 在 $L^2[0, 2\pi]$ 上稠密。

#### Lem 2. (三角多项式的稠密性)
有理系数的三角多项式函数在 $C[0, 2\pi]$ 上稠密。

#### Cor. (三角函数系的稠密性)
三角函数系 $\{ \frac{1}{\sqrt{2\pi}}, \cos t, \sin t, \dots \}$ 在 $L^2[0, 2\pi]$ 上稠密。

#### Thm 4. (Fourier 级数定理)
三角函数系 $\{ \frac{1}{\sqrt{2\pi}}, \cos t, \sin t, \dots \}$ 是 $L^2[0, 2\pi]$ 上的一个标准正交基，因此 $\forall x \in L^2[0, 2\pi], x = \sum_{n=1}^\infty (x, e_i) e_i = a_0 + \sum_{i=1}^\infty a_i \cos it + b_i \sin it$.
事实上是 Fourier 级数，$a_i = \frac{1}{\pi} \int_0^{2\pi} x(t) \cos it dt, b_i = \frac{1}{\pi} \int_0^{2\pi} x(t) \sin it dt$.

---

## 总结

本笔记共包含：
- **定理 (Thm)**: 约 30 个
- **命题 (Prop)**: 约 10 个
- **推论 (Cor)**: 约 15 个
- **引理 (Lem)**: 约 3 个

**总计约 58 个主要定理、命题、推论和引理。**

