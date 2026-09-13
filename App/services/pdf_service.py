from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from sqlalchemy.orm import Session

from App.database.models.crop import Crop
from App.database.models.farm import Farm
from App.database.models.cost import Cost
from App.database.models.harvest import Harvest
from App.database.models.sale import Sale


def generate_crop_pdf(
    db: Session,
    crop_id: int,
    current_farmer_id: int
):
    """
    Tengeneza PDF ya ripoti ya zao moja.

    PDF ina:
    - Taarifa za shamba
    - Taarifa za zao
    - Gharama
    - Mavuno
    - Mauzo
    - Muhtasari wa fedha
    """

    # =========================
    # 1. TAFUTA ZAO
    # =========================

    crop = (
        db.query(Crop)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Crop.id == crop_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if crop is None:
        return None

    farm = crop.farm

    # =========================
    # 2. PATA GHARAMA
    # =========================

    costs = (
        db.query(Cost)
        .filter(
            Cost.crop_id == crop_id
        )
        .order_by(Cost.tarehe.asc())
        .all()
    )

    total_cost = sum(
        cost.gharama
        for cost in costs
    )

    # =========================
    # 3. PATA MAVUNO
    # =========================

    harvests = (
        db.query(Harvest)
        .filter(
            Harvest.crop_id == crop_id
        )
        .order_by(Harvest.tarehe.asc())
        .all()
    )

    total_harvest = sum(
        harvest.kiasi
        for harvest in harvests
    )

    harvest_units = set(
        harvest.unit
        for harvest in harvests
    )

    if len(harvest_units) == 1:
        harvest_unit = next(iter(harvest_units))
    elif len(harvest_units) == 0:
        harvest_unit = "-"
    else:
        harvest_unit = "mchanganyiko"

    # =========================
    # 4. PATA MAUZO
    # =========================

    harvest_ids = [
        harvest.id
        for harvest in harvests
    ]

    if harvest_ids:
        sales = (
            db.query(Sale)
            .filter(
                Sale.harvest_id.in_(harvest_ids)
            )
            .order_by(Sale.tarehe.asc())
            .all()
        )
    else:
        sales = []

    total_sales_quantity = sum(
        sale.kiasi
        for sale in sales
    )

    sale_units = set(
        sale.unit
        for sale in sales
    )

    if len(sale_units) == 1:
        sale_unit = next(iter(sale_units))
    elif len(sale_units) == 0:
        sale_unit = "-"
    else:
        sale_unit = "mchanganyiko"

    total_revenue = sum(
        sale.jumla
        for sale in sales
    )

    # =========================
    # 5. FAIDA / HASARA
    # =========================

    profit_loss = total_revenue - total_cost

    if profit_loss > 0:
        hali = "FAIDA"
    elif profit_loss < 0:
        hali = "HASARA"
    else:
        hali = "SAWA"

    # =========================
    # 6. TENGENEZA PDF
    # =========================

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        spaceAfter=10,
    )

    section_style = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        alignment=TA_LEFT,
        spaceBefore=8,
        spaceAfter=6,
    )

    normal_style = ParagraphStyle(
        "NormalText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
    )

    # =========================
    # 7. CONTENT YA PDF
    # =========================

    story = []

    story.append(
        Paragraph(
            "MKULIMA SMART ASSISTANT",
            title_style
        )
    )

    story.append(
        Paragraph(
            "RIPOTI YA UZALISHAJI WA ZAO",
            title_style
        )
    )

    story.append(Spacer(1, 5))

    # =========================
    # TAARIFA ZA SHAMBA
    # =========================

    story.append(
        Paragraph(
            "1. TAARIFA ZA SHAMBA",
            section_style
        )
    )

    farm_data = [
        ["Jina la shamba", farm.jina],
        ["Eneo", farm.eneo],
        ["Ukubwa", f"{farm.ukubwa}"],
    ]

    farm_table = Table(
        farm_data,
        colWidths=[55 * mm, 115 * mm]
    )

    farm_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ])
    )

    story.append(farm_table)

    # =========================
    # TAARIFA ZA ZAO
    # =========================

    story.append(
        Paragraph(
            "2. TAARIFA ZA ZAO",
            section_style
        )
    )

    crop_data = [
        ["Zao", crop.jina],
        ["Aina", crop.aina],
        ["Msimu", crop.msimu or "-"],
        [
            "Tarehe ya kupanda",
            str(crop.tarehe_ya_kupanda)
            if crop.tarehe_ya_kupanda
            else "-"
        ],
    ]

    crop_table = Table(
        crop_data,
        colWidths=[55 * mm, 115 * mm]
    )

    crop_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ])
    )

    story.append(crop_table)

    # =========================
    # GHARAMA
    # =========================

    story.append(
        Paragraph(
            "3. GHARAMA",
            section_style
        )
    )

    if costs:
        cost_data = [
            [
                "Tarehe",
                "Jina",
                "Aina",
                "Kiasi",
                "Gharama"
            ]
        ]

        for cost in costs:
            quantity = (
                f"{cost.kiasi} {cost.unit}"
                if cost.kiasi is not None
                else "-"
            )

            cost_data.append([
                str(cost.tarehe),
                cost.jina,
                cost.aina,
                quantity,
                f"TSh {cost.gharama:,.2f}",
            ])

        cost_table = Table(
            cost_data,
            colWidths=[
                27 * mm,
                32 * mm,
                27 * mm,
                35 * mm,
                40 * mm,
            ],
            repeatRows=1
        )

        cost_table.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ])
        )

        story.append(cost_table)

    else:
        story.append(
            Paragraph(
                "Hakuna gharama zilizorekodiwa.",
                normal_style
            )
        )

    story.append(Spacer(1, 5))

    story.append(
        Paragraph(
            f"Jumla ya gharama: TSh {total_cost:,.2f}",
            normal_style
        )
    )

    # =========================
    # MAVUNO
    # =========================

    story.append(
        Paragraph(
            "4. MAVUNO",
            section_style
        )
    )

    if harvests:
        harvest_data = [
            [
                "Tarehe",
                "Kiasi",
                "Unit",
                "Maelezo"
            ]
        ]

        for harvest in harvests:
            harvest_data.append([
                str(harvest.tarehe),
                f"{harvest.kiasi}",
                harvest.unit,
                harvest.maelezo or "-"
            ])

        harvest_table = Table(
            harvest_data,
            colWidths=[
                35 * mm,
                30 * mm,
                30 * mm,
                66 * mm,
            ],
            repeatRows=1
        )

        harvest_table.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ])
        )

        story.append(harvest_table)

    else:
        story.append(
            Paragraph(
                "Hakuna mavuno yaliyorekodiwa.",
                normal_style
            )
        )

    story.append(Spacer(1, 5))

    story.append(
        Paragraph(
            f"Jumla ya mavuno: {total_harvest} {harvest_unit}",
            normal_style
        )
    )

    # =========================
    # MAUZO
    # =========================

    story.append(
        Paragraph(
            "5. MAUZO",
            section_style
        )
    )

    if sales:
        sales_data = [
            [
                "Tarehe",
                "Kiasi",
                "Unit",
                "Bei/Unit",
                "Jumla"
            ]
        ]

        for sale in sales:
            sales_data.append([
                str(sale.tarehe),
                f"{sale.kiasi}",
                sale.unit,
                f"TSh {sale.bei_kwa_unit:,.2f}",
                f"TSh {sale.jumla:,.2f}",
            ])

        sales_table = Table(
            sales_data,
            colWidths=[
                32 * mm,
                25 * mm,
                25 * mm,
                42 * mm,
                42 * mm,
            ],
            repeatRows=1
        )

        sales_table.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ])
        )

        story.append(sales_table)

    else:
        story.append(
            Paragraph(
                "Hakuna mauzo yaliyorekodiwa.",
                normal_style
            )
        )

    story.append(Spacer(1, 5))

    story.append(
        Paragraph(
            f"Jumla iliyouzwa: "
            f"{total_sales_quantity} {sale_unit}",
            normal_style
        )
    )

    story.append(
        Paragraph(
            f"Jumla ya mapato: TSh {total_revenue:,.2f}",
            normal_style
        )
    )

    # =========================
    # MUHTASARI WA FEDHA
    # =========================

    story.append(
        Paragraph(
            "6. MUHTASARI WA FEDHA",
            section_style
        )
    )

    financial_data = [
        ["Jumla ya gharama", f"TSh {total_cost:,.2f}"],
        ["Jumla ya mapato", f"TSh {total_revenue:,.2f}"],
        ["Faida / Hasara", f"TSh {profit_loss:,.2f}"],
        ["Hali", hali],
    ]

    financial_table = Table(
        financial_data,
        colWidths=[70 * mm, 100 * mm]
    )

    financial_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ])
    )

    story.append(financial_table)

    # =========================
    # FOOTER
    # =========================

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "Ripoti imetengenezwa na Mkulima Smart Assistant.",
            normal_style
        )
    )

    # =========================
    # BUILD PDF
    # =========================

    document.build(story)

    buffer.seek(0)

    return buffer