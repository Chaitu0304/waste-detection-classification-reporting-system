import os
from pathlib import Path
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_user_waste_report(
    detected_items=None, 
    image_name="image_1.jpg", 
    output_folder="results"
):
    """
    Generates a dynamically-named User PDF Report and CSV log
    based on the source image name (e.g., waste_report_image_1.pdf).
    """
    out_dir = Path(output_folder)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Extract the clean image identifier (e.g. 'image_1.jpg' -> 'image_1')
    image_stem = Path(image_name).stem
    report_base_name = f"waste_report_{image_stem}"

    # 2. Sample/Fallback detection list if none is passed from live inference
    if not detected_items:
        detected_items = [
            {"Item_ID": f"{image_stem.upper()}-01", "Category": "PLASTIC", "Confidence": 0.94, "Type": "Recyclable (Dry Waste)"},
            {"Item_ID": f"{image_stem.upper()}-02", "Category": "PLASTIC", "Confidence": 0.88, "Type": "Recyclable (Dry Waste)"},
            {"Item_ID": f"{image_stem.upper()}-03", "Category": "GLASS", "Confidence": 0.91, "Type": "Recyclable (Bottles/Jars)"},
            {"Item_ID": f"{image_stem.upper()}-04", "Category": "BIODEGRADABLE", "Confidence": 0.85, "Type": "Organic / Wet Compost"},
            {"Item_ID": f"{image_stem.upper()}-05", "Category": "BIODEGRADABLE", "Confidence": 0.79, "Type": "Organic / Wet Compost"},
            {"Item_ID": f"{image_stem.upper()}-06", "Category": "METAL", "Confidence": 0.92, "Type": "Recyclable (Scrap/Can)"},
            {"Item_ID": f"{image_stem.upper()}-07", "Category": "CARDBOARD", "Confidence": 0.86, "Type": "Recyclable (Dry Paperboard)"},
            {"Item_ID": f"{image_stem.upper()}-08", "Category": "PAPER", "Confidence": 0.76, "Type": "Recyclable (Clean Paper)"},
        ]

    df_items = pd.DataFrame(detected_items)
    total_count = len(df_items)
    category_counts = df_items["Category"].value_counts()
    dominant_category = category_counts.index[0] if total_count > 0 else "N/A"
    
    bio_count = len(df_items[df_items["Category"] == "BIODEGRADABLE"])
    recyclable_count = total_count - bio_count
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 3. Export CSV using the image name (e.g. waste_report_image_1.csv)
    csv_path = out_dir / f"{report_base_name}.csv"
    df_items.to_csv(csv_path, index=False)
    print(f"[OK] CSV Log saved as: {csv_path}")

    # 4. Generate High-Quality PDF using the image name (e.g. waste_report_image_1.pdf)
    pdf_path = out_dir / f"{report_base_name}.pdf"
    
    fig, ax = plt.subplots(figsize=(8.5, 11), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Background Base
    ax.add_patch(patches.Rectangle((0, 0), 100, 100, facecolor='#F8FAFC', zorder=0))

    # Header Top Banner
    ax.add_patch(patches.Rectangle((0, 88), 100, 12, facecolor='#1E3A8A', zorder=1))
    ax.text(5, 95.5, f"WASTE DETECTION REPORT: {image_stem.upper()}", fontsize=15, weight='bold', color='white')
    ax.text(5, 91.5, f"Source File: {image_name}   |   Generated: {timestamp}   |   Model: YOLOv8s", fontsize=8.5, color='#93C5FD')

    # Top KPI Metrics Cards
    def draw_kpi(x, y, w, h, title, val, b_color, text_color):
        ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5", facecolor='white', edgecolor=b_color, linewidth=1.5, zorder=2))
        ax.text(x + w/2, y + h - 2.8, title.upper(), fontsize=7.5, weight='bold', color='#64748B', ha='center', zorder=3)
        ax.text(x + w/2, y + 2.2, str(val), fontsize=13, weight='bold', color=text_color, ha='center', zorder=3)

    draw_kpi(5,  77, 20, 8.5, "Total Objects", total_count, '#3B82F6', '#1E40AF')
    draw_kpi(28, 77, 20, 8.5, "Dominant Type", dominant_category, '#059669', '#065F46')
    draw_kpi(51, 77, 20, 8.5, "Dry Recyclable", recyclable_count, '#D97706', '#92400E')
    draw_kpi(74, 77, 21, 8.5, "Wet / Compost", bio_count, '#10B981', '#065F46')

    # SECTION 1: Summary Table
    ax.text(5, 73.5, "1. Waste Category Breakdown & Facility Sorting Stream", fontsize=10.5, weight='bold', color='#0F172A')

    summary_headers = ["Waste Category", "Instances", "Share (%)", "Disposal Stream / Facility Action"]
    all_cats = ['BIODEGRADABLE', 'CARDBOARD', 'GLASS', 'METAL', 'PAPER', 'PLASTIC']
    
    table_rows = []
    for cat in all_cats:
        cnt = int(category_counts.get(cat, 0))
        pct = f"{(cnt / total_count * 100):.1f}%" if total_count > 0 else "0.0%"
        dest = "Organic Green Bin -> Municipal Compost Plant" if cat == "BIODEGRADABLE" else "Blue Bin -> Automated Material Recovery Facility (MRF)"
        table_rows.append([cat, str(cnt), pct, dest])
    
    table_rows.append(["OVERALL TOTAL", str(total_count), "100.0%", f"Image {image_stem} Batch Complete"])

    # Render Section 1 Custom Table Grid
    col_x = [5, 27, 41, 55, 95]
    row_y = 69.5
    row_h = 3.2

    # Draw Summary Header
    ax.add_patch(patches.Rectangle((5, row_y), 90, row_h, facecolor='#334155', edgecolor='#334155', zorder=2))
    for i in range(len(summary_headers)):
        align = 'center' if i in [1, 2] else 'left'
        pos_x = (col_x[i] + col_x[i+1])/2 if i in [1, 2] else col_x[i] + 1.5
        ax.text(pos_x, row_y + 1.0, summary_headers[i], color='white', weight='bold', fontsize=7.5, ha=align, zorder=3)

    # Draw Summary Rows
    for r_idx, r_data in enumerate(table_rows):
        row_y -= row_h
        is_last = (r_idx == len(table_rows) - 1)
        bg = '#E2E8F0' if is_last else ('#FFFFFF' if r_idx % 2 == 0 else '#F1F5F9')
        ax.add_patch(patches.Rectangle((5, row_y), 90, row_h, facecolor=bg, edgecolor='#CBD5E1', linewidth=0.6, zorder=2))
        
        for c_idx, val in enumerate(r_data):
            align = 'center' if c_idx in [1, 2] else 'left'
            pos_x = (col_x[c_idx] + col_x[c_idx+1])/2 if c_idx in [1, 2] else col_x[c_idx] + 1.5
            font_wt = 'bold' if is_last or c_idx == 0 else 'normal'
            t_color = '#1E3A8A' if (is_last and c_idx == 0) else '#1E293B'
            ax.text(pos_x, row_y + 0.9, val, color=t_color, weight=font_wt, fontsize=7.5, ha=align, zorder=3)

    # SECTION 2: Itemized Detection Log
    ax.text(5, 41.5, f"2. Itemized Detections for {image_name}", fontsize=10.5, weight='bold', color='#0F172A')

    log_headers = ["Item ID", "Category Label", "Model Confidence", "Recyclability Classification"]
    log_col_x = [5, 23, 45, 65, 95]
    log_row_y = 37.5
    log_row_h = 3.0

    # Draw Log Header
    ax.add_patch(patches.Rectangle((5, log_row_y), 90, log_row_h, facecolor='#475569', edgecolor='#475569', zorder=2))
    for i in range(len(log_headers)):
        align = 'center' if i in [0, 2] else 'left'
        pos_x = (log_col_x[i] + log_col_x[i+1])/2 if i in [0, 2] else log_col_x[i] + 1.5
        ax.text(pos_x, log_row_y + 0.9, log_headers[i], color='white', weight='bold', fontsize=7.5, ha=align, zorder=3)

    # Draw Log Rows
    for r_idx, row in df_items.head(8).iterrows():
        log_row_y -= log_row_h
        bg = '#FFFFFF' if r_idx % 2 == 0 else '#F8FAFC'
        ax.add_patch(patches.Rectangle((5, log_row_y), 90, log_row_h, facecolor=bg, edgecolor='#CBD5E1', linewidth=0.6, zorder=2))

        vals = [row["Item_ID"], row["Category"], f"{row['Confidence']*100:.1f}%", row["Type"]]
        for c_idx, val in enumerate(vals):
            align = 'center' if c_idx in [0, 2] else 'left'
            pos_x = (log_col_x[c_idx] + log_col_x[c_idx+1])/2 if c_idx in [0, 2] else log_col_x[c_idx] + 1.5
            font_wt = 'bold' if c_idx in [0, 1] else 'normal'
            t_color = '#0284C7' if c_idx == 2 else '#1E293B'
            ax.text(pos_x, log_row_y + 0.8, val, color=t_color, weight=font_wt, fontsize=7.2, ha=align, zorder=3)

    # Footer Banner
    ax.add_patch(patches.Rectangle((0, 0), 100, 5, facecolor='#0F172A', zorder=1))
    ax.text(50, 1.8, f"Smart Waste Detection System | Generated for {image_name} | Operations Console", 
            fontsize=7.5, color='#94A3B8', ha='center', zorder=2)

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig(pdf_path, format='pdf', dpi=300)
    plt.close()

    print(f"[OK] PDF Report saved as: {pdf_path}")

if __name__ == "__main__":
    # Test with image 1
    generate_user_waste_report(image_name="image_1.jpg")