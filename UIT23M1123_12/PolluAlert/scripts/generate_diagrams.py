import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ArrowStyle, BoxStyle

FIGURES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

# Common styling constants
COLOR_PRIMARY = "#1E3A8A"    # Dark Navy
COLOR_SECONDARY = "#0284C7"  # Cyan Blue
COLOR_ACCENT = "#0D9488"     # Teal
COLOR_WARN = "#EA580C"       # Orange
COLOR_ALERT = "#DC2626"      # Red
COLOR_BG_BOX = "#F8FAFC"     # Light background
COLOR_BORDER = "#475569"     # Slate border
FONT_FAMILY = "sans-serif"

def draw_box(ax, x, y, w, h, title, subtitle="", bg="#EFF6FF", border="#1D4ED8", rad=0.03, lw=1.5, title_color="#1E3A8A"):
    box = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={rad}", fc=bg, ec=border, lw=lw, zorder=2)
    ax.add_patch(box)
    if subtitle:
        ax.text(x + w/2, y + h*0.62, title, ha="center", va="center", fontsize=9.5, fontweight="bold", color=title_color, family=FONT_FAMILY, zorder=3)
        ax.text(x + w/2, y + h*0.30, subtitle, ha="center", va="center", fontsize=7.5, color="#334155", family=FONT_FAMILY, zorder=3)
    else:
        ax.text(x + w/2, y + h/2, title, ha="center", va="center", fontsize=9, fontweight="bold", color=title_color, family=FONT_FAMILY, zorder=3)

def draw_arrow(ax, x1, y1, x2, y2, label="", color="#475569", lw=1.5, rad=0.0):
    connectionstyle = f"arc3,rad={rad}" if rad != 0 else "arc3,rad=0"
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=14, connectionstyle=connectionstyle),
        zorder=4
    )
    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2 + 0.02
        ax.text(mx, my, label, ha="center", va="bottom", fontsize=7.5, color="#1E293B", backgroundcolor="#FFFFFFEE", family=FONT_FAMILY, zorder=5)

# -------------------------------------------------------------
# 1. Figure 4.1: System Architecture Diagram
# -------------------------------------------------------------
def generate_architecture():
    fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    ax.text(0.5, 0.96, "Figure 4.1: PolluAlert Multi-Tier Layered System Architecture", ha="center", fontsize=13, fontweight="bold", color=COLOR_PRIMARY)

    layers = [
        ("PRESENTATION LAYER (STREAMLIT WEB UI)", 0.74, "#EFF6FF", "#3B82F6", [
            ("Home View", "Overview & Mission", 0.08),
            ("Incident Analysis", "Text Input & Evaluation", 0.38),
            ("Analytics Dashboard", "Metrics, Charts, Map", 0.68)
        ]),
        ("APPLICATION LOGIC & ORCHESTRATION LAYER", 0.50, "#F0FDF4", "#22C55E", [
            ("Prediction Controller", "predict_complaint()", 0.08),
            ("Hybrid Severity Engine", "ML + Heuristic Boosting", 0.38),
            ("Information Extraction", "Regex & spaCy NER", 0.68)
        ]),
        ("NLP & MACHINE LEARNING INFERENCE LAYER", 0.26, "#FAF5FF", "#A855F7", [
            ("Text Preprocessing", "Cleaning, Negation, Lemmatization", 0.08),
            ("TF-IDF Vectorizer", "Unigram + Bigram (5k features)", 0.38),
            ("ML Model Ensemble", "Naive Bayes, LogReg, Linear SVM", 0.68)
        ]),
        ("DATA STORAGE & PERSISTENCE LAYER", 0.02, "#FFFBEB", "#F59E0B", [
            ("SQLite DB (pollualert.db)", "Incidents, Entities, Feedback", 0.08),
            ("Model Artifacts (*.pkl)", "Trained Models & Vectorizers", 0.38),
            ("Datasets & Logs", "CSV Corpora & Evaluation Logs", 0.68)
        ]),
    ]

    for title, ly, bg, border, boxes in layers:
        big_box = FancyBboxPatch((0.04, ly), 0.92, 0.18, boxstyle="round,pad=0.015", fc=bg, ec=border, lw=1.5, zorder=1)
        ax.add_patch(big_box)
        ax.text(0.06, ly + 0.15, title, fontsize=9.5, fontweight="bold", color=border, family=FONT_FAMILY)
        for b_title, b_sub, bx in boxes:
            draw_box(ax, bx, ly + 0.025, 0.24, 0.10, b_title, b_sub, bg="#FFFFFF", border=border, lw=1)

    # Inter-layer connection arrows
    for y in [0.74, 0.50, 0.26]:
        draw_arrow(ax, 0.5, y, 0.5, y - 0.04, lw=2, color=COLOR_PRIMARY)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig_4_1_architecture.png"), bbox_inches="tight")
    plt.close()

# -------------------------------------------------------------
# 2. Figure 4.3: Context-Level DFD (Level 0)
# -------------------------------------------------------------
def generate_dfd_level_0():
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    ax.text(0.5, 0.93, "Figure 4.3: Level-0 Context-Level Data Flow Diagram", ha="center", fontsize=13, fontweight="bold", color=COLOR_PRIMARY)

    # Entities
    draw_box(ax, 0.05, 0.42, 0.18, 0.16, "Citizen / Complainant", "[External Entity]", bg="#FEF3C7", border="#D97706")
    draw_box(ax, 0.77, 0.60, 0.18, 0.16, "Response Authority", "[Emergency Team / CPCB]", bg="#FEF3C7", border="#D97706")
    draw_box(ax, 0.77, 0.24, 0.18, 0.16, "Municipal Officer", "[Admin / Investigator]", bg="#FEF3C7", border="#D97706")

    # Central Process (Circle)
    circ = patches.Circle((0.5, 0.5), 0.14, fc="#EFF6FF", ec="#1D4ED8", lw=2.5, zorder=2)
    ax.add_patch(circ)
    ax.text(0.5, 0.53, "0.0", ha="center", va="center", fontsize=11, fontweight="bold", color="#1D4ED8")
    ax.text(0.5, 0.47, "PolluAlert NLP\nSystem", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#1E3A8A")

    # Flows
    draw_arrow(ax, 0.23, 0.53, 0.36, 0.53, "Raw Pollution Report Text", color="#2563EB")
    draw_arrow(ax, 0.36, 0.45, 0.23, 0.45, "Incident Confirmation & Summary", color="#059669")
    draw_arrow(ax, 0.63, 0.56, 0.77, 0.65, "High-Severity Emergency Alerts", color="#DC2626", lw=2)
    draw_arrow(ax, 0.63, 0.44, 0.77, 0.32, "Classified Logs & Analytics", color="#2563EB")

    # Data store
    draw_box(ax, 0.41, 0.10, 0.18, 0.10, "D1: SQLite Database", "pollualert.db", bg="#F1F5F9", border="#475569")
    draw_arrow(ax, 0.5, 0.36, 0.5, 0.20, "Store / Query", color="#475569")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig_4_3_dfd_level_0.png"), bbox_inches="tight")
    plt.close()

# -------------------------------------------------------------
# 3. Figure 4.4: Level-1 DFD
# -------------------------------------------------------------
def generate_dfd_level_1():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    ax.text(0.5, 0.95, "Figure 4.4: Level-1 Data Flow Diagram (Main Subsystems)", ha="center", fontsize=13, fontweight="bold", color=COLOR_PRIMARY)

    # User
    draw_box(ax, 0.03, 0.65, 0.15, 0.14, "Citizen / User", "External Entity", bg="#FEF3C7", border="#D97706")

    # Processes
    draw_box(ax, 0.26, 0.65, 0.18, 0.14, "1.0 Text Preprocessing", "Clean, Tokenize, Lemmatize", bg="#EFF6FF", border="#2563EB")
    draw_box(ax, 0.54, 0.65, 0.18, 0.14, "2.0 Feature Extraction", "TF-IDF Vectorizer (5k)", bg="#EFF6FF", border="#2563EB")
    draw_box(ax, 0.78, 0.65, 0.18, 0.14, "3.0 Classification", "Multi-Target ML Models", bg="#EFF6FF", border="#2563EB")

    draw_box(ax, 0.78, 0.25, 0.18, 0.14, "4.0 Severity & Emergency", "Rule-Based Boosting", bg="#FEF2F2", border="#EF4444")
    draw_box(ax, 0.45, 0.25, 0.20, 0.14, "5.0 Entity & Summary", "Locations, Pollutants, Text", bg="#F0FDF4", border="#16A34A")

    # Data Store
    draw_box(ax, 0.15, 0.25, 0.20, 0.14, "D1: SQLite Database", "Incident & Feedback Logs", bg="#F1F5F9", border="#475569")

    # Flows
    draw_arrow(ax, 0.18, 0.72, 0.26, 0.72, "Raw Text")
    draw_arrow(ax, 0.44, 0.72, 0.54, 0.72, "Clean Tokens")
    draw_arrow(ax, 0.72, 0.72, 0.78, 0.72, "TF-IDF Matrix")
    draw_arrow(ax, 0.87, 0.65, 0.87, 0.39, "Predicted Probabilities")
    draw_arrow(ax, 0.78, 0.32, 0.65, 0.32, "Severity Score")
    draw_arrow(ax, 0.45, 0.32, 0.35, 0.32, "Persist Record")
    draw_arrow(ax, 0.25, 0.39, 0.10, 0.65, "Render Report & Status", color="#059669")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig_4_4_dfd_level_1.png"), bbox_inches="tight")
    plt.close()

# -------------------------------------------------------------
# 4. Figure 4.5: Level-2 DFD
# -------------------------------------------------------------
def generate_dfd_level_2():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    ax.text(0.5, 0.95, "Figure 4.5: Level-2 DFD — Subsystem Processing Decomposition", ha="center", fontsize=13, fontweight="bold", color=COLOR_PRIMARY)

    draw_box(ax, 0.05, 0.55, 0.20, 0.15, "3.1 Pollution Classification", "Multinomial NB / LogReg\n(Air, Water, Noise, Waste...)", bg="#EFF6FF", border="#2563EB")
    draw_box(ax, 0.40, 0.70, 0.20, 0.15, "3.2 Severity Prediction", "Multi-Class ML Model\n(Low, Med, High, Critical)", bg="#EFF6FF", border="#2563EB")
    draw_box(ax, 0.40, 0.38, 0.20, 0.15, "3.3 Emergency Detector", "Binary Classifier\n(Emergency: 0 or 1)", bg="#EFF6FF", border="#2563EB")

    draw_box(ax, 0.74, 0.70, 0.21, 0.15, "3.4 Rule-Based Severity Boost", "Dangerous Keywords Match\n(+Score Adjustment)", bg="#FEF2F2", border="#EF4444")
    draw_box(ax, 0.74, 0.38, 0.21, 0.15, "3.5 Rule-Based Emergency Escalation", "Hospital / Gas Leak Keywords\n(Forces Critical Trigger)", bg="#FEF2F2", border="#EF4444")

    draw_box(ax, 0.40, 0.08, 0.55, 0.14, "3.6 Entity & Information Synthesis", "Regex Landmark Matching + spaCy Entity Extraction + Summary Generator", bg="#F0FDF4", border="#16A34A")

    # Arrows
    draw_arrow(ax, 0.25, 0.65, 0.40, 0.75, "Features")
    draw_arrow(ax, 0.25, 0.60, 0.40, 0.45, "Features")
    draw_arrow(ax, 0.60, 0.77, 0.74, 0.77, "Raw Severity")
    draw_arrow(ax, 0.60, 0.45, 0.74, 0.45, "Raw Emergency")
    draw_arrow(ax, 0.84, 0.70, 0.84, 0.22, "Adjusted Severity")
    draw_arrow(ax, 0.74, 0.40, 0.65, 0.22, "Emergency Flag")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig_4_5_dfd_level_2.png"), bbox_inches="tight")
    plt.close()

# -------------------------------------------------------------
# 5. Figure 4.6: Use Case Diagram
# -------------------------------------------------------------
def generate_use_case():
    fig, ax = plt.subplots(figsize=(9, 7), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    ax.text(0.5, 0.95, "Figure 4.6: UML Use Case Diagram for PolluAlert", ha="center", fontsize=13, fontweight="bold", color=COLOR_PRIMARY)

    # System Boundary
    boundary = FancyBboxPatch((0.24, 0.06), 0.52, 0.84, boxstyle="round,pad=0.02", fc="#F8FAFC", ec="#64748B", lw=2, linestyle="--")
    ax.add_patch(boundary)
    ax.text(0.50, 0.87, "PolluAlert System Boundary", ha="center", fontsize=10, fontweight="bold", color="#334155")

    # Actors
    draw_box(ax, 0.03, 0.68, 0.16, 0.12, "Citizen", "Complainant", bg="#FEF3C7", border="#D97706")
    draw_box(ax, 0.03, 0.28, 0.16, 0.12, "Field Officer", "First Responder", bg="#FEF3C7", border="#D97706")
    draw_box(ax, 0.81, 0.44, 0.17, 0.14, "Administrator", "Environmental\nAuthority", bg="#FEF3C7", border="#D97706")

    use_cases = [
        ("Submit Pollution Complaint", 0.78),
        ("View Live Automated Analysis", 0.66),
        ("Receive Emergency SMS/Alert", 0.54),
        ("Browse Filterable Incident Logs", 0.42),
        ("Submit Validation Feedback", 0.30),
        ("View Real-Time Analytics Dashboard", 0.18),
        ("Retrain / Monitor ML Models", 0.09)
    ]

    for uc, y in use_cases:
        ellipse = patches.Ellipse((0.50, y), 0.44, 0.07, fc="#EFF6FF", ec="#2563EB", lw=1.5, zorder=3)
        ax.add_patch(ellipse)
        ax.text(0.50, y, uc, ha="center", va="center", fontsize=8.5, fontweight="bold", color="#1E3A8A", zorder=4)

    # Connections Citizen
    for y in [0.78, 0.66, 0.54]:
        ax.plot([0.15, 0.28], [0.73, y], color="#475569", lw=1.2)

    # Connections Officer
    for y in [0.54, 0.42, 0.30]:
        ax.plot([0.15, 0.28], [0.32, y], color="#475569", lw=1.2)

    # Connections Admin
    for y in [0.42, 0.30, 0.18, 0.09]:
        ax.plot([0.85, 0.72], [0.52, y], color="#475569", lw=1.2)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig_4_6_use_case.png"), bbox_inches="tight")
    plt.close()

# -------------------------------------------------------------
# 6. Figure 4.7: Activity Diagram
# -------------------------------------------------------------
def generate_activity_diagram():
    fig, ax = plt.subplots(figsize=(8, 9), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    ax.text(0.5, 0.96, "Figure 4.7: UML Activity Diagram — Incident Processing Workflow", ha="center", fontsize=12, fontweight="bold", color=COLOR_PRIMARY)

    # Start Node
    ax.add_patch(patches.Circle((0.5, 0.91), 0.02, fc="#000000", ec="#000000"))

    steps = [
        ("Enter Complaint Text in Web UI", 0.82),
        ("Preprocess Text (Clean, Tokenize, Lemmatize)", 0.71),
        ("Extract TF-IDF N-Gram Vector (5,000 Dim)", 0.60),
        ("Perform Multi-Target Model Inference", 0.49),
    ]

    draw_arrow(ax, 0.5, 0.89, 0.5, 0.86)
    for i, (st, y) in enumerate(steps):
        draw_box(ax, 0.18, y, 0.64, 0.07, st, bg="#EFF6FF", border="#2563EB")
        if i < len(steps) - 1:
            draw_arrow(ax, 0.5, y, 0.5, steps[i+1][1] + 0.07)

    # Decision Diamond
    draw_arrow(ax, 0.5, 0.49, 0.5, 0.43)
    diamond = patches.Polygon([[0.5, 0.43], [0.62, 0.38], [0.5, 0.33], [0.38, 0.38]], fc="#FEF3C7", ec="#D97706", lw=1.5)
    ax.add_patch(diamond)
    ax.text(0.5, 0.38, "Is Emergency\nScore >= 0.70?", ha="center", va="center", fontsize=7.5, fontweight="bold", color="#92400E")

    # Branches
    draw_arrow(ax, 0.62, 0.38, 0.78, 0.38, "[Yes]")
    draw_box(ax, 0.65, 0.24, 0.28, 0.08, "Trigger Emergency Alert\n& Escalate Priority", bg="#FEE2E2", border="#DC2626")
    draw_arrow(ax, 0.79, 0.34, 0.79, 0.32)

    draw_arrow(ax, 0.38, 0.38, 0.22, 0.38, "[No]")
    draw_box(ax, 0.07, 0.24, 0.28, 0.08, "Assign Standard Queue\n& Log Incident", bg="#F0FDF4", border="#16A34A")
    draw_arrow(ax, 0.21, 0.34, 0.21, 0.32)

    # Join Node
    draw_box(ax, 0.25, 0.11, 0.50, 0.065, "Store Record in SQLite & Render UI", bg="#F1F5F9", border="#475569")
    draw_arrow(ax, 0.21, 0.24, 0.38, 0.175)
    draw_arrow(ax, 0.79, 0.24, 0.62, 0.175)

    # End Node
    draw_arrow(ax, 0.5, 0.11, 0.5, 0.05)
    ax.add_patch(patches.Circle((0.5, 0.035), 0.02, fc="#FFFFFF", ec="#000000", lw=1.5))
    ax.add_patch(patches.Circle((0.5, 0.035), 0.012, fc="#000000", ec="#000000"))

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig_4_7_activity_diagram.png"), bbox_inches="tight")
    plt.close()

# -------------------------------------------------------------
# 7. Figure 4.8: Sequence Diagram
# -------------------------------------------------------------
def generate_sequence_diagram():
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    ax.text(0.5, 0.96, "Figure 4.8: UML Sequence Diagram for Complaint Processing", ha="center", fontsize=13, fontweight="bold", color=COLOR_PRIMARY)

    lifelines = [
        ("User / Citizen", 0.10),
        ("Streamlit UI", 0.30),
        ("Prediction Controller", 0.50),
        ("NLP & ML Engine", 0.70),
        ("SQLite Database", 0.90),
    ]

    for title, x in lifelines:
        draw_box(ax, x - 0.08, 0.86, 0.16, 0.065, title, bg="#EFF6FF", border="#2563EB")
        ax.plot([x, x], [0.86, 0.08], color="#94A3B8", linestyle="--", lw=1.2)

    calls = [
        (0.10, 0.30, 0.78, "submit_complaint(text)"),
        (0.30, 0.50, 0.71, "predict_complaint(text)"),
        (0.50, 0.70, 0.64, "clean_and_vectorize(text)"),
        (0.70, 0.70, 0.57, "model.predict_proba() [Self]"),
        (0.70, 0.50, 0.50, "return class_predictions"),
        (0.50, 0.90, 0.42, "save_complaint(record)"),
        (0.90, 0.50, 0.34, "return record_id & status"),
        (0.50, 0.30, 0.26, "return prediction_dict"),
        (0.30, 0.10, 0.18, "display_results & alert banner"),
    ]

    for x1, x2, y, label in calls:
        if x1 == x2:
            ax.annotate("", xy=(x1, y - 0.03), xytext=(x1, y), arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=1.2, connectionstyle="arc,angleA=0,armA=20,rad=10"))
            ax.text(x1 + 0.04, y - 0.015, label, fontsize=7.5, color="#DC2626", fontweight="bold")
        else:
            style = "-|>"
            ls = "-" if x1 < x2 else "--"
            ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle=style, color="#1E293B", lw=1.3, linestyle=ls))
            ax.text((x1 + x2)/2, y + 0.015, label, ha="center", fontsize=7.5, color="#1E3A8A", backgroundcolor="#FFFFFFDD")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig_4_8_sequence_diagram.png"), bbox_inches="tight")
    plt.close()

# -------------------------------------------------------------
# 8. Figure 4.9: Class Diagram
# -------------------------------------------------------------
def generate_class_diagram():
    fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    ax.text(0.5, 0.96, "Figure 4.9: UML Class Diagram for PolluAlert System", ha="center", fontsize=13, fontweight="bold", color=COLOR_PRIMARY)

    classes = [
        ("TextPreprocessor", 0.05, 0.58, 0.26, 0.30, [
            "+ stopwords: set",
            "+ lemmatizer: WordNetLemmatizer",
            "------------------------",
            "+ clean_text(text): str",
            "+ tokenize(text): list",
            "+ remove_stopwords(tokens): list",
            "+ lemmatize(tokens): list"
        ]),
        ("TFIDFExtractor", 0.37, 0.58, 0.26, 0.30, [
            "+ max_features: int = 5000",
            "+ ngram_range: tuple = (1, 2)",
            "+ vectorizer: TfidfVectorizer",
            "------------------------",
            "+ fit_transform(corpus): matrix",
            "+ transform(text): array",
            "+ save(path): void"
        ]),
        ("MLClassifierEnsemble", 0.69, 0.58, 0.26, 0.30, [
            "+ pollution_model: LogisticRegression",
            "+ severity_model: LinearSVC",
            "+ emergency_model: MultinomialNB",
            "------------------------",
            "+ train(X_train, y_train): void",
            "+ predict(features): dict",
            "+ evaluate(X_test, y_test): dict"
        ]),
        ("EntityExtractor", 0.05, 0.12, 0.26, 0.30, [
            "+ location_patterns: list",
            "+ pollutant_lexicon: dict",
            "------------------------",
            "+ extract_locations(text): list",
            "+ extract_pollutants(text): list",
            "+ extract_sources(text): list",
            "+ extract_contact(text): list"
        ]),
        ("SeverityEngine", 0.37, 0.12, 0.26, 0.30, [
            "+ emergency_keywords: set",
            "+ severity_weights: dict",
            "------------------------",
            "+ calculate_severity(text): str",
            "+ check_emergency(text, score): bool",
            "+ recommend_action(type, sev): str"
        ]),
        ("DatabaseManager", 0.69, 0.12, 0.26, 0.30, [
            "+ db_path: str = 'pollualert.db'",
            "------------------------",
            "+ init_db(): void",
            "+ save_complaint(record): int",
            "+ get_recent(limit): DataFrame",
            "+ update_feedback(id, flag): void"
        ]),
    ]

    for name, x, y, w, h, members in classes:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01", fc="#F8FAFC", ec="#2563EB", lw=1.5)
        ax.add_patch(box)
        # Header banner
        header = FancyBboxPatch((x, y + h - 0.05), w, 0.05, boxstyle="round,pad=0.01", fc="#1E3A8A", ec="#1E3A8A")
        ax.add_patch(header)
        ax.text(x + w/2, y + h - 0.025, name, ha="center", va="center", fontsize=9, fontweight="bold", color="#FFFFFF")
        
        # Text members
        my = y + h - 0.075
        for m in members:
            ax.text(x + 0.015, my, m, fontsize=7.5, fontfamily="monospace", color="#1E293B", va="top")
            my -= 0.032

    # Associations
    ax.plot([0.31, 0.37], [0.73, 0.73], color="#475569", lw=1.5)
    ax.plot([0.63, 0.69], [0.73, 0.73], color="#475569", lw=1.5)
    ax.plot([0.31, 0.37], [0.27, 0.27], color="#475569", lw=1.5)
    ax.plot([0.63, 0.69], [0.27, 0.27], color="#475569", lw=1.5)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig_4_9_class_diagram.png"), bbox_inches="tight")
    plt.close()

# -------------------------------------------------------------
# 9. Figure 4.10: ER Diagram
# -------------------------------------------------------------
def generate_er_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    ax.text(0.5, 0.95, "Figure 4.10: Entity-Relationship (ER) Schema Diagram", ha="center", fontsize=13, fontweight="bold", color=COLOR_PRIMARY)

    tables = [
        ("COMPLAINTS", 0.08, 0.45, 0.24, 0.38, [
            "PK: id (INTEGER)",
            "raw_text (TEXT)",
            "cleaned_text (TEXT)",
            "timestamp (DATETIME)",
            "source_type (VARCHAR)",
            "reporter_phone (VARCHAR)"
        ]),
        ("PREDICTIONS", 0.40, 0.45, 0.24, 0.38, [
            "PK: id (INTEGER)",
            "FK: complaint_id (INTEGER)",
            "pollution_type (VARCHAR)",
            "confidence_score (FLOAT)",
            "severity_level (VARCHAR)",
            "severity_score (FLOAT)",
            "is_emergency (BOOLEAN)",
            "recommended_action (TEXT)"
        ]),
        ("ENTITIES", 0.72, 0.45, 0.24, 0.38, [
            "PK: id (INTEGER)",
            "FK: complaint_id (INTEGER)",
            "entity_type (VARCHAR)",
            "entity_value (TEXT)",
            "start_char (INTEGER)",
            "end_char (INTEGER)"
        ]),
        ("FEEDBACK_LOGS", 0.40, 0.06, 0.24, 0.28, [
            "PK: id (INTEGER)",
            "FK: complaint_id (INTEGER)",
            "user_validation (BOOLEAN)",
            "corrected_category (VARCHAR)",
            "review_notes (TEXT)",
            "reviewed_at (DATETIME)"
        ])
    ]

    for name, x, y, w, h, cols in tables:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01", fc="#F8FAFC", ec="#0369A1", lw=1.5)
        ax.add_patch(box)
        header = FancyBboxPatch((x, y + h - 0.06), w, 0.06, boxstyle="round,pad=0.01", fc="#0369A1", ec="#0369A1")
        ax.add_patch(header)
        ax.text(x + w/2, y + h - 0.03, name, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#FFFFFF")
        
        my = y + h - 0.09
        for c in cols:
            color = "#B91C1C" if "PK:" in c else ("#0D9488" if "FK:" in c else "#1E293B")
            fw = "bold" if ("PK:" in c or "FK:" in c) else "normal"
            ax.text(x + 0.015, my, c, fontsize=8, fontfamily="monospace", color=color, fontweight=fw, va="top")
            my -= 0.036

    # 1:1 and 1:N Relationships
    draw_arrow(ax, 0.32, 0.64, 0.40, 0.64, "1 : 1", color="#2563EB", lw=2)
    draw_arrow(ax, 0.64, 0.64, 0.72, 0.64, "1 : N", color="#2563EB", lw=2)
    draw_arrow(ax, 0.52, 0.45, 0.52, 0.34, "1 : N", color="#2563EB", lw=2)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig_4_10_er_diagram.png"), bbox_inches="tight")
    plt.close()

# -------------------------------------------------------------
# 10. Figure 6.1: NLP Pipeline Flowchart
# -------------------------------------------------------------
def generate_nlp_pipeline():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    ax.text(0.5, 0.95, "Figure 6.1: Complete End-to-End NLP Pipeline Flowchart", ha="center", fontsize=13, fontweight="bold", color=COLOR_PRIMARY)

    nodes = [
        ("Raw Text Input", 0.03, 0.42, 0.12, 0.16, "#FEF3C7", "#D97706"),
        ("Noise Removal\n& Lowercase", 0.18, 0.42, 0.12, 0.16, "#EFF6FF", "#2563EB"),
        ("Tokenize &\nNegation Filter", 0.33, 0.42, 0.12, 0.16, "#EFF6FF", "#2563EB"),
        ("WordNet\nLemmatization", 0.48, 0.42, 0.12, 0.16, "#EFF6FF", "#2563EB"),
        ("TF-IDF Vectorize\n(1-gram + 2-gram)", 0.63, 0.42, 0.13, 0.16, "#FAF5FF", "#9333EA"),
        ("Multi-Classifier\nEnsemble", 0.79, 0.42, 0.14, 0.16, "#F0FDF4", "#16A34A"),
    ]

    for title, x, y, w, h, bg, border in nodes:
        draw_box(ax, x, y, w, h, title, bg=bg, border=border, lw=1.5)

    for i in range(len(nodes) - 1):
        x1 = nodes[i][1] + nodes[i][3]
        x2 = nodes[i+1][1]
        draw_arrow(ax, x1, 0.50, x2, 0.50, lw=2, color="#475569")

    # Outputs
    draw_arrow(ax, 0.86, 0.58, 0.86, 0.78)
    draw_box(ax, 0.74, 0.78, 0.24, 0.12, "Pollution Classification\n(Air, Water, Noise...)", bg="#EFF6FF", border="#2563EB")

    draw_arrow(ax, 0.93, 0.50, 0.97, 0.50)
    draw_box(ax, 0.74, 0.18, 0.24, 0.12, "Severity & Emergency\n(Low, Med, High, Critical)", bg="#FEF2F2", border="#DC2626")
    draw_arrow(ax, 0.86, 0.42, 0.86, 0.30)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig_6_1_nlp_pipeline.png"), bbox_inches="tight")
    plt.close()

# -------------------------------------------------------------
# 11. Figure 6.2: TF-IDF Process
# -------------------------------------------------------------
def generate_tfidf_process():
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    ax.text(0.5, 0.94, "Figure 6.2: TF-IDF Feature Extraction Process & Term Weighting", ha="center", fontsize=13, fontweight="bold", color=COLOR_PRIMARY)

    draw_box(ax, 0.05, 0.60, 0.25, 0.20, "Preprocessed Document", "Tokens: ['chemical', 'leak',\n'industrial', 'area']", bg="#EFF6FF", border="#2563EB")
    draw_box(ax, 0.38, 0.60, 0.26, 0.20, "N-Gram Generator", "Unigrams: 'chemical', 'leak'\nBigrams: 'chemical leak'", bg="#FAF5FF", border="#9333EA")
    draw_box(ax, 0.72, 0.60, 0.24, 0.20, "Vocabulary Dictionary", "Top 5,000 Frequent\nDistinct Features", bg="#F0FDF4", border="#16A34A")

    draw_arrow(ax, 0.30, 0.70, 0.38, 0.70)
    draw_arrow(ax, 0.64, 0.70, 0.72, 0.70)

    # Formula Box
    draw_box(ax, 0.20, 0.12, 0.60, 0.32, "TF-IDF Mathematical Weighting Formula", 
             "TF(t, d) = f(t, d) / sum(f(t', d))\nIDF(t, D) = ln((1 + |D|) / (1 + |{d in D : t in d}|)) + 1\nTF-IDF(t, d, D) = TF(t, d) * IDF(t, D)\nL2 Normalization applied to vector length",
             bg="#FFFBEB", border="#D97706")
    draw_arrow(ax, 0.84, 0.60, 0.60, 0.44)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig_6_2_tfidf_process.png"), bbox_inches="tight")
    plt.close()

# -------------------------------------------------------------
# 12. Figure 6.3: Implementation Flowchart
# -------------------------------------------------------------
def generate_implementation_flowchart():
    fig, ax = plt.subplots(figsize=(8, 9), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    ax.text(0.5, 0.97, "Figure 6.3: Implementation Flowchart of Complete System", ha="center", fontsize=12, fontweight="bold", color=COLOR_PRIMARY)

    nodes = [
        ("Receive Input Complaint Text", 0.88),
        ("Sanitize & Validate Text Length", 0.78),
        ("Preprocess Text (NLTK Tokenizer & Lemmatizer)", 0.68),
        ("Vectorize with Fitted TF-IDF Model", 0.58),
        ("Execute ML Classification (Pollution, Severity, Emergency)", 0.48),
        ("Run Regex & NER for Location / Entity Extraction", 0.38),
        ("Apply Heuristic Rule-Based Severity Adjustments", 0.28),
        ("Store Incident in SQLite & Return Structured JSON", 0.18),
        ("Display Real-Time Visual Alerts on Streamlit Web UI", 0.08)
    ]

    for i, (text, y) in enumerate(nodes):
        draw_box(ax, 0.15, y, 0.70, 0.065, text, bg="#EFF6FF", border="#2563EB")
        if i < len(nodes) - 1:
            draw_arrow(ax, 0.5, y, 0.5, nodes[i+1][1] + 0.065, color="#475569")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig_6_3_implementation_flowchart.png"), bbox_inches="tight")
    plt.close()

def main():
    print("Generating diagrams...")
    generate_architecture()
    generate_dfd_level_0()
    generate_dfd_level_1()
    generate_dfd_level_2()
    generate_use_case()
    generate_activity_diagram()
    generate_sequence_diagram()
    generate_class_diagram()
    generate_er_diagram()
    generate_nlp_pipeline()
    generate_tfidf_process()
    generate_implementation_flowchart()
    print("All diagrams generated successfully in:", FIGURES_DIR)

if __name__ == "__main__":
    main()
