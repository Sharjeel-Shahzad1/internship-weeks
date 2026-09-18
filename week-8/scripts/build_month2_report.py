"""
Generate Month 2 Comprehensive Internship Report (Month2_Report.docx).

Internship: Arch Technologies, Machine Learning Domain, Month 2
Author: Sharjeel Shahzad
Tasks Covered:
- Task 3: California Housing Price Prediction (Weeks 5 & 6)
- Task 4: Iris Flower Classification (Weeks 7 & 8)
"""

from __future__ import annotations

import os
from pathlib import Path

import docx
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor


def set_cell_background(cell, fill_hex: str) -> None:
    """Set background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150) -> None:
    """Set inner padding margins of a table cell (in twips, 20 twips = 1 pt)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def add_callout(doc, text: str, title: str = "KEY TAKEAWAY") -> None:
    """Add a stylized callout box."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

    # Set left border thick blue, remove others
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="1F497D"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r_title = p.add_run(f"[{title}] ")
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
    r_title.font.size = Pt(10)

    r_text = p.add_run(text)
    r_text.font.size = Pt(10)
    r_text.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    doc.add_paragraph()  # spacing


def format_table_headers(table, col_widths=None) -> None:
    """Style table header row with Arch Technologies blue."""
    for idx, cell in enumerate(table.rows[0].cells):
        set_cell_background(cell, "1F497D")
        set_cell_margins(cell, top=140, bottom=140, left=150, right=150)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.bold = True
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                run.font.size = Pt(9.5)


def style_table_rows(table, col_widths=None) -> None:
    """Style table data rows with alternating shading."""
    for r_idx, row in enumerate(table.rows[1:], start=1):
        bg = "F9FBFD" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, cell in enumerate(row.cells):
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(0x22, 0x22, 0x22)


def add_figure_with_caption(doc, img_path: Path, caption: str, width: float = 6.0) -> None:
    """Safely embed image with centered caption."""
    if not img_path.exists():
        p_missing = doc.add_paragraph(f"[Image not found: {img_path.name}]")
        p_missing.runs[0].font.italic = True
        return

    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(2)
    run_img = p_img.add_run()
    run_img.add_picture(str(img_path), width=Inches(width))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(12)
    r_cap = p_cap.add_run(caption)
    r_cap.font.size = Pt(9)
    r_cap.font.italic = True
    r_cap.font.color.rgb = RGBColor(0x55, 0x55, 0x55)


def build_report() -> Path:
    """Compile Month2_Report.docx end-to-end."""
    repo_root = Path(__file__).resolve().parents[2]
    outputs_dir = repo_root / "week-8" / "outputs"
    output_path = outputs_dir / "Month2_Report.docx"

    doc = docx.Document()

    # Set 1-inch margins
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # Base font setup
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Calibri'
    font.size = Pt(10.5)
    font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # -------------------------------------------------------------
    # FRONT PAGE / TITLE BLOCK (Arch Technologies Guidelines)
    # -------------------------------------------------------------
    p_org = doc.add_paragraph()
    p_org.paragraph_format.space_before = Pt(0)
    p_org.paragraph_format.space_after = Pt(4)
    r_org = p_org.add_run("ARCH TECHNOLOGIES | MACHINE LEARNING INTERNSHIP")
    r_org.font.size = Pt(11)
    r_org.font.bold = True
    r_org.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("MONTH 2 FINAL INTERNSHIP PROJECT REPORT")
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x16, 0x36, 0x5C)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub = p_sub.add_run(
        "Comprehensive Technical Synthesis of Task 3: California Housing Price Prediction (Weeks 5 & 6)\n"
        "and Task 4: Iris Flower Classification (Weeks 7 & 8)"
    )
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

    # Metadata Box
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Intern Full Name:", "Sharjeel Shahzad"),
        ("Internship Domain:", "Machine Learning"),
        ("Email Address:", "ssharjeel160@gmail.com"),
        ("Contact Phone:", "+92-300-1234567"),
        ("Submission Milestone:", "Month 2 Final Comprehensive Deliverable (Weeks 5 – 8)"),
    ]

    for idx, (label, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        set_cell_background(row.cells[0], "F2F4F8")
        set_cell_background(row.cells[1], "FAFAFA")
        set_cell_margins(row.cells[0], top=80, bottom=80, left=120, right=120)
        set_cell_margins(row.cells[1], top=80, bottom=80, left=120, right=120)

        p0 = row.cells[0].paragraphs[0]
        r0 = p0.add_run(label)
        r0.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

        p1 = row.cells[1].paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.size = Pt(9.5)
        r1.font.bold = (idx == 0 or idx == 4)

    doc.add_paragraph()  # Spacing
    doc.add_page_break()

    # -------------------------------------------------------------
    # SECTION 1: MONTH 2 EXECUTIVE OVERVIEW
    # -------------------------------------------------------------
    h1 = doc.add_heading("1. Executive Summary & Month 2 Overview", level=1)
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "During Month 2 of the Arch Technologies Machine Learning Internship, two end-to-end industry-grade machine "
        "learning pipelines were formulated, executed, evaluated, and productionized. The curriculum spanned four intensive weeks "
        "divided between two distinct predictive machine learning paradigms:"
    )

    doc.add_paragraph(
        "• Task 3: California Housing Price Prediction (Weeks 5 & 6) — High-dimensional continuous regression, spatial-demographic "
        "feature engineering, collinearity resolution, and benchmarking ordinary linear regression against non-linear tree ensembles "
        "(Random Forest and Gradient Boosting Regressors) with cross-validated hyperparameter optimization.",
        style='List Bullet'
    )
    doc.add_paragraph(
        "• Task 4: Iris Flower Classification (Weeks 7 & 8) — Supervised botanical multiclass classification, morphological "
        "distribution exploration, continuous feature standardization, linear baseline modeling (Logistic Regression), and "
        "comparative benchmarking of advanced classifiers (K-Nearest Neighbors, Decision Trees, Support Vector Machines) "
        "with non-linear RBF kernel margin tuning.",
        style='List Bullet'
    )

    add_callout(
        doc,
        "Month 2 achieved 100% production artifact completion across all deliverables: complete repository tracking, "
        "zero data leakage via strict split-first feature engineering, full hyperparameter cross-validation, and "
        "production model serializations with standalone runnable scripts and fully executed Jupyter notebooks.",
        "MILESTONE HIGHLIGHT"
    )

    # Overview Table
    ov_table = doc.add_table(rows=5, cols=4)
    ov_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    ov_headers = ["Task Identifier", "Domain & Dataset", "Champion Model", "Key Test Result"]
    for i, title in enumerate(ov_headers):
        ov_table.rows[0].cells[i].paragraphs[0].text = title

    task_summary_rows = [
        ("Task 3 (Weeks 5-6)", "Continuous Regression\n(California Housing, 20.6k records)", "Tuned Random Forest\n(150 trees, max_features=None)", "RMSE: $49,666.10\nR² Score: 0.8215"),
        ("Task 4 (Weeks 7-8)", "Multiclass Classification\n(UCI Iris, 150 specimens)", "Tuned Support Vector Classifier\n(RBF Kernel, C=2.0, γ=0.05)", "Test Accuracy: 100.0%\nMacro F1: 1.0000"),
        ("Regression Gain", "Over Linear Baseline", "30.78% RMSE Error Reduction", "+29.31% R² Variance Explained"),
        ("Classification Gain", "Over Linear Overlap", "Non-Linear Soft Margin Hyperplane", "Clean Versicolor-Virginica Separation"),
    ]

    for r_idx, row_vals in enumerate(task_summary_rows, start=1):
        for c_idx, val in enumerate(row_vals):
            ov_table.rows[r_idx].cells[c_idx].paragraphs[0].text = val

    format_table_headers(ov_table)
    style_table_rows(ov_table)
    doc.add_paragraph()

    # -------------------------------------------------------------
    # SECTION 2: TASK 3 - HOUSING PRICE PREDICTION (WEEKS 5 & 6)
    # -------------------------------------------------------------
    doc.add_page_break()
    h2 = doc.add_heading("2. Task 3: California Housing Price Prediction (Weeks 5 & 6)", level=1)
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(6)

    doc.add_heading("2.1 Objective & Dataset Characteristics", level=2)
    doc.add_paragraph(
        "The objective of Task 3 was to construct an accurate predictive regression model to estimate median house values "
        "(`median_house_value`) across California census block groups using demographic, geographic, and housing features. "
        "The raw dataset comprised 20,640 block group observations with 10 original features: longitude, latitude, "
        "housing median age, total rooms, total bedrooms, population, households, median income, and ocean proximity."
    )

    doc.add_heading("2.2 Data Preprocessing & Feature Engineering Pipeline", level=2)
    doc.add_paragraph(
        "Raw district totals (e.g., total rooms, total bedrooms, population) reflect neighborhood cluster size rather than individual "
        "living quality. To establish predictive parity and alleviate severe multicollinearity, a rigorous feature engineering pipeline "
        "was executed during Week 5:"
    )
    doc.add_paragraph(
        "1. Imputation: Missing values in `total_bedrooms` (207 records, ~1%) were imputed using the median of training data to "
        "prevent data leakage.\n"
        "2. Engineered Density Metrics: Ratios were derived to reflect household living standards:\n"
        "   - rooms_per_household = total_rooms / households\n"
        "   - bedrooms_per_room = total_bedrooms / total_rooms\n"
        "   - population_per_household = population / households\n"
        "3. Categorical Encoding: One-hot encoded `ocean_proximity` (e.g., INLAND, <1H OCEAN, NEAR BAY, NEAR OCEAN), dropping one "
        "category to avoid the dummy variable trap.\n"
        "4. Feature Standardization: Transformed continuous variables with `StandardScaler` fitted on the 80% training partition (16,512 samples), "
        "holding out 20% (4,128 samples) as an untouched test benchmark."
    )

    # Embed Heatmap
    heatmap_path = repo_root / "week-5" / "outputs" / "correlation_heatmap.png"
    add_figure_with_caption(
        doc,
        heatmap_path,
        "Figure 1: Task 3 Feature Correlation Heatmap highlighting strong positive relationship between median_income and median_house_value (r = 0.69).",
        width=5.5
    )

    doc.add_heading("2.3 Model Exploration & Advanced Ensembles", level=2)
    doc.add_paragraph(
        "During Week 5, a Multiple Linear Regression baseline was trained, yielding an RMSE of $71,750.18 and R² of 0.6353. "
        "While serviceable, linear formulations cannot accommodate non-linear spatial dependencies (latitude/longitude interactions) "
        "or non-linear diminishing returns of income. In Week 6, two powerful ensemble paradigms were implemented:"
    )
    doc.add_paragraph(
        "• Random Forest Regressor: A bagging ensemble of decorrelated decision trees that samples features randomly at each candidate split, "
        "reducing variance and handling outliers naturally.\n"
        "• Gradient Boosting Regressor: A sequential boosting ensemble fitting shallow decision trees to pseudo-residuals of preceding trees "
        "via gradient descent in function space."
    )

    doc.add_heading("2.4 Hyperparameter Tuning & Cross-Validation", level=2)
    doc.add_paragraph(
        "Random Forest emerged as the superior ensemble. To maximize generalization and restrict tree memorization, 3-fold cross-validated "
        "`GridSearchCV` was executed across tree count (`n_estimators`: 100, 150), depth limits (`max_depth`: 20, None), and split thresholds "
        "(`min_samples_split`: 2, 5). The optimal architecture (`n_estimators=150`, `max_depth=None`, `min_samples_split=2`) achieved "
        "an out-of-fold cross-validation RMSE of $51,037.68."
    )

    doc.add_heading("2.5 Task 3 Benchmark Results & Error Diagnostics", level=2)
    doc.add_paragraph(
        "The final tuned Random Forest model achieved state-of-the-art performance on the 4,128 unseen test instances:"
    )

    t3_table = doc.add_table(rows=5, cols=5)
    t3_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    t3_headers = ["Model Configuration", "Model Paradigm", "Test RMSE ($)", "Test MAE ($)", "Test R² Score"]
    for i, title in enumerate(t3_headers):
        t3_table.rows[0].cells[i].paragraphs[0].text = title

    t3_results = [
        ("Multiple Linear Regression", "Linear Baseline (Week 5)", "$71,750.18", "$52,006.98", "0.6353"),
        ("Gradient Boosting Regressor", "Sequential Boosting (Week 6)", "$57,393.75", "$39,521.10", "0.7616"),
        ("Default Random Forest", "Bagging Ensemble (Week 6)", "$49,780.29", "$32,150.44", "0.8207"),
        ("Tuned Random Forest", "Optimized Ensemble (Champion)", "$49,666.10", "$32,027.45", "0.8215"),
    ]

    for r_idx, row_vals in enumerate(t3_results, start=1):
        for c_idx, val in enumerate(row_vals):
            t3_table.rows[r_idx].cells[c_idx].paragraphs[0].text = val

    format_table_headers(t3_table)
    style_table_rows(t3_table)
    doc.add_paragraph()

    # Embed Week 6 Comparison & Prediction plots
    t3_comp_chart = repo_root / "week-6" / "outputs" / "model_comparison_chart.png"
    add_figure_with_caption(
        doc,
        t3_comp_chart,
        "Figure 2: Task 3 Comparative Model Evaluation (RMSE, MAE, R²) demonstrating substantial error reduction achieved by Random Forest.",
        width=5.8
    )

    t3_pred_chart = repo_root / "week-6" / "outputs" / "sample_predictions.png"
    add_figure_with_caption(
        doc,
        t3_pred_chart,
        "Figure 3: Task 3 Predicted vs. Actual Housing Price diagnostic scatter plot and residual distribution showing tight alignment along identity line.",
        width=5.8
    )

    add_callout(
        doc,
        "Residual diagnostic analysis revealed that prediction error increases primarily near the artificial census survey ceiling "
        "at $500,001. Random Forest successfully accommodated this discontinuity without distorting predictions for homes under $450,000.",
        "RESIDUAL ANALYSIS"
    )

    # -------------------------------------------------------------
    # SECTION 3: TASK 4 - IRIS FLOWER CLASSIFICATION (WEEKS 7 & 8)
    # -------------------------------------------------------------
    doc.add_page_break()
    h3 = doc.add_heading("3. Task 4: Iris Flower Classification (Weeks 7 & 8)", level=1)
    h3.paragraph_format.space_before = Pt(12)
    h3.paragraph_format.space_after = Pt(6)

    doc.add_heading("3.1 Objective & Morphological Domain Properties", level=2)
    doc.add_paragraph(
        "Task 4 focused on botanical species classification using Sir Ronald Fisher's benchmark Iris dataset. "
        "The problem entails predicting the precise iris species (*Iris-setosa*, *Iris-versicolor*, or *Iris-virginica*) "
        "from four physical measurements: Sepal Length, Sepal Width, Petal Length, and Petal Width (all in centimeters). "
        "The raw dataset contains 150 perfectly balanced observations (50 per species)."
    )

    doc.add_heading("3.2 Exploratory Data Analysis & Class Separability", level=2)
    doc.add_paragraph(
        "Comprehensive EDA in Week 7 revealed essential geometric properties of the feature space:\n"
        "• Non-informative Feature Removal: The raw `Id` column was discarded prior to modeling.\n"
        "• Linear Separability of Setosa: Across all bivariate feature projections involving petal dimensions, *Iris-setosa* forms a "
        "completely detached, linearly separable cluster (Petal Length < 2.0 cm, Petal Width < 0.6 cm).\n"
        "• Complex Boundary Overlap: *Iris-versicolor* and *Iris-virginica* exhibit overlapping marginal distributions in sepal length and width, "
        "requiring precise decision boundaries to resolve subtle boundary points.\n"
        "• Biological Variance: Boxplot and IQR analysis identified four statistical anomalies in Sepal Width; these were verified as natural "
        "biological morphology and retained to preserve botanical variance."
    )

    # Embed Pairplot
    pairplot_path = repo_root / "week-7" / "outputs" / "pairplot.png"
    add_figure_with_caption(
        doc,
        pairplot_path,
        "Figure 4: Task 4 Pairwise Feature Distribution Grid showing clear linear clustering for Setosa and overlapping regions between Versicolor and Virginica.",
        width=5.5
    )

    doc.add_heading("3.3 Baseline Classifier (Week 7)", level=2)
    doc.add_paragraph(
        "In Week 7, a multinomial Logistic Regression baseline was implemented with `StandardScaler` preprocessing. On the held-out "
        "20% test split (30 instances), the model achieved 100% test accuracy. However, training set evaluation revealed 4 misclassifications "
        "(96.67% train accuracy) located directly on the linear hyperplane separating Versicolor and Virginica, establishing the motivation "
        "for Week 8's non-linear classifier benchmarking."
    )

    cm_week7_path = repo_root / "week-7" / "outputs" / "confusion_matrix.png"
    add_figure_with_caption(
        doc,
        cm_week7_path,
        "Figure 5: Week 7 Baseline Logistic Regression Test Set Confusion Matrix.",
        width=4.5
    )

    doc.add_heading("3.4 Advanced Classifiers & Hyperparameter Tuning (Week 8)", level=2)
    doc.add_paragraph(
        "In Week 8, three advanced classification paradigms were trained on the preprocessed training partition (`week-7/outputs/X_train.csv`):\n"
        "1. K-Nearest Neighbors (KNN): Non-parametric instance-based voting (`n_neighbors=5`, Minkowski distance).\n"
        "2. Decision Tree (CART): Recursive non-linear axis-orthogonal space partitioning (`criterion='gini'`).\n"
        "3. Support Vector Machine (SVM): Maximal soft-margin hyperplane with non-linear kernel transformations.\n\n"
        "SVM was selected as the champion architecture. To optimize margin softness and kernel curvature, exhaustive 5-fold stratified "
        "`GridSearchCV` was performed across `kernel` (linear, rbf, poly), `C` (0.1 to 50.0), and `gamma` (0.05 to 1.0). The optimal "
        "hyperparameter configuration discovered was:\n"
        "   kernel='rbf', C=2.0, gamma=0.05 (Mean 5-Fold CV Accuracy: 96.67%, std: 0.0167)."
    )

    doc.add_heading("3.5 Final Task 4 Comparative Evaluation", level=2)
    doc.add_paragraph(
        "Evaluating all models on the held-out test partition (30 specimens: 10 Setosa, 9 Versicolor, 11 Virginica) produced "
        "impeccable classification fidelity across all four evaluation metrics:"
    )

    t4_table = doc.add_table(rows=6, cols=6)
    t4_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    t4_headers = ["Model Architecture", "Paradigm / Family", "Accuracy", "Macro Precision", "Macro Recall", "Macro F1"]
    for i, title in enumerate(t4_headers):
        t4_table.rows[0].cells[i].paragraphs[0].text = title

    t4_results = [
        ("Logistic Regression (Week 7)", "Linear Maximum Likelihood", "100.00%", "1.0000", "1.0000", "1.0000"),
        ("K-Nearest Neighbors (k=5)", "Instance-Based Distance", "100.00%", "1.0000", "1.0000", "1.0000"),
        ("Decision Tree (CART)", "Recursive Orthogonal Split", "100.00%", "1.0000", "1.0000", "1.0000"),
        ("Support Vector Machine (Default)", "RBF Kernel Margin (C=1.0)", "100.00%", "1.0000", "1.0000", "1.0000"),
        ("Tuned Support Vector Machine", "Optimized RBF Margin (Champion)", "100.00%", "1.0000", "1.0000", "1.0000"),
    ]

    for r_idx, row_vals in enumerate(t4_results, start=1):
        for c_idx, val in enumerate(row_vals):
            t4_table.rows[r_idx].cells[c_idx].paragraphs[0].text = val

    format_table_headers(t4_table)
    style_table_rows(t4_table)
    doc.add_paragraph()

    # Embed Week 8 Comparison Chart & Sample Predictions
    t4_comp_chart = repo_root / "week-8" / "outputs" / "model_comparison_chart.png"
    add_figure_with_caption(
        doc,
        t4_comp_chart,
        "Figure 6: Task 4 Classifier Performance Comparison across Accuracy, Precision, Recall, and F1-score.",
        width=5.8
    )

    t4_pred_chart = repo_root / "week-8" / "outputs" / "sample_predictions.png"
    add_figure_with_caption(
        doc,
        t4_pred_chart,
        "Figure 7: Final Tuned SVM Test Predictions table and Confusion Matrix heatmap confirming 100% classification accuracy.",
        width=6.0
    )

    # -------------------------------------------------------------
    # SECTION 4: TECHNICAL COMPARATIVE SYNTHESIS
    # -------------------------------------------------------------
    doc.add_page_break()
    h4 = doc.add_heading("4. Comparative Synthesis: Regression vs. Classification", level=1)
    h4.paragraph_format.space_before = Pt(12)
    h4.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Synthesizing Tasks 3 and 4 provides profound practical insights into the contrasting mechanics of continuous regression "
        "and discrete multiclass classification:"
    )

    comp_table = doc.add_table(rows=6, cols=3)
    comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_headers = ["Engineering Dimension", "Task 3: Housing Price Prediction", "Task 4: Iris Flower Classification"]
    for i, title in enumerate(c_headers):
        comp_table.rows[0].cells[i].paragraphs[0].text = title

    c_rows = [
        ("Predictive Goal", "Predict continuous numeric value ($)\n[Range: $14,999 – $500,001]", "Predict discrete categorical class\n[3 balanced botanical species]"),
        ("Loss Formulation", "Mean Squared Error (L2 penalty) &\nMean Absolute Error (L1 penalty)", "Cross-Entropy Loss &\nMaximal Soft-Margin Hinge Loss"),
        ("Feature Engineering Impact", "Crucial: Engineered ratio features resolved severe cluster-size multicollinearity", "Standardization: Scaled dimensions to prevent Euclidean metric distortion"),
        ("Overfitting Dynamics", "Mitigated via tree bagging and constraining leaf sample split thresholds", "Mitigated via 5-fold stratified CV and margin regularization penalty (C)"),
        ("Champion Architecture", "Tuned Random Forest Regressor\n(RMSE: $49,666.10, R²: 0.8215)", "Tuned Support Vector Classifier\n(Accuracy: 100.0%, F1: 1.0000)"),
    ]

    for r_idx, row_vals in enumerate(c_rows, start=1):
        for c_idx, val in enumerate(row_vals):
            comp_table.rows[r_idx].cells[c_idx].paragraphs[0].text = val

    format_table_headers(comp_table)
    style_table_rows(comp_table)
    doc.add_paragraph()

    # -------------------------------------------------------------
    # SECTION 5: CONCLUSION & ROADMAP
    # -------------------------------------------------------------
    h5 = doc.add_heading("5. Month 2 Conclusion & Next Steps", level=1)
    h5.paragraph_format.space_before = Pt(12)
    h5.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Month 2 has concluded with complete mastery of regression and classification engineering workflows. All required models, "
        "scripts, evaluation notebooks, and visual artifacts have been fully validated and saved to their respective directories:\n"
        "• Standalone reproducible training pipelines (`train_advanced_models.py`, `train_advanced_classifiers.py`).\n"
        "• Self-contained serialized models (`housing_rf_model_tuned.pkl`, `iris_svm_model_tuned.pkl`).\n"
        "• Executed diagnostic notebooks (`housing_evaluation.ipynb`, `iris_evaluation.ipynb`).\n"
        "• Structured documentation and testing summaries across all weeks."
    )

    doc.add_paragraph(
        "With Tasks 3 and 4 officially closed and Month 2 finalized, preparation begins for Month 3 curriculum challenges, which will "
        "advance into unsupervised clustering, dimensionality reduction, and deep learning architectures."
    )

    # Save document
    doc.save(str(output_path))
    print(f"[+] Successfully generated Month 2 Report -> {output_path} ({output_path.stat().st_size} bytes)")
    return output_path


if __name__ == "__main__":
    build_report()
