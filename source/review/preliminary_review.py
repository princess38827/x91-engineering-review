#!/usr/bin/env python3
"""Generate the X-91 pre-fabrication review calculations and PDF dossier."""

from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "review" / "X91_Pre-Fabrication_Review_Dossier_v0.2.pdf"


def calculations(config: dict) -> dict:
    mass_kg = config["mass"]["maximum_concept_kg"]
    gravity = config["environment"]["gravity_m_s2"]
    span_m = config["geometry"]["span_m"]
    limit_positive_g = 3.5
    ultimate_factor = 1.5
    ultimate_g = limit_positive_g * ultimate_factor
    ultimate_lift_n = mass_kg * gravity * ultimate_g
    # Conservative preliminary half-wing root moment using the resultant lift
    # at 42 percent of semispan. This is a requirement, not a spar capacity.
    root_moment_nm = (ultimate_lift_n / 2.0) * (0.42 * span_m / 2.0)
    return {
        "maximum_mass_kg": mass_kg,
        "positive_limit_load_g": limit_positive_g,
        "ultimate_factor": ultimate_factor,
        "positive_ultimate_load_g": ultimate_g,
        "ultimate_total_lift_n": ultimate_lift_n,
        "preliminary_root_bending_moment_each_side_nm": root_moment_nm,
        "battery_nominal_energy_wh": (
            config["propulsion"]["battery_nominal_voltage_v"]
            * config["propulsion"]["battery_capacity_ah"]
        ),
    }


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#59636e"))
    canvas.drawString(0.65 * inch, 0.42 * inch, "X-91 PRE-FABRICATION REVIEW - PRELIMINARY / NOT A CERTIFICATION")
    canvas.drawRightString(7.85 * inch, 0.42 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf(config: dict, calc: dict) -> None:
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=25, leading=29, alignment=TA_CENTER, textColor=colors.HexColor("#102a43"),
        spaceAfter=16,
    ))
    styles.add(ParagraphStyle(
        name="Section", parent=styles["Heading1"], fontName="Helvetica-Bold",
        fontSize=16, leading=19, textColor=colors.HexColor("#0b7285"), spaceBefore=8, spaceAfter=10,
    ))
    styles.add(ParagraphStyle(
        name="Sub", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=11.5, leading=14, textColor=colors.HexColor("#243b53"), spaceBefore=7, spaceAfter=5,
    ))
    styles.add(ParagraphStyle(name="BodyX", parent=styles["BodyText"], fontSize=9.3, leading=13, spaceAfter=7))
    styles.add(ParagraphStyle(name="SmallX", parent=styles["BodyText"], fontSize=8, leading=10.5))
    styles.add(ParagraphStyle(
        name="Banner", parent=styles["BodyText"], fontName="Helvetica-Bold",
        fontSize=12, leading=16, alignment=TA_CENTER, textColor=colors.white,
        backColor=colors.HexColor("#b42318"), borderPadding=10, spaceBefore=12, spaceAfter=12,
    ))

    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=letter, rightMargin=0.62 * inch, leftMargin=0.62 * inch,
        topMargin=0.62 * inch, bottomMargin=0.65 * inch,
        title="X-91 Pre-Fabrication Review Dossier v0.2",
        author="Preliminary engineering analysis prepared for independent review",
    )
    story = []
    story.append(Spacer(1, 0.65 * inch))
    story.append(Paragraph("BLACK MANTA X-91", styles["CoverTitle"]))
    story.append(Paragraph("Civilian Scale Flight Demonstrator", ParagraphStyle(
        name="CoverSub", parent=styles["Heading2"], alignment=TA_CENTER,
        fontSize=15, leading=19, textColor=colors.HexColor("#334e68"), spaceAfter=24,
    )))
    story.append(Paragraph("PRE-FABRICATION REVIEW DOSSIER - VERSION 0.2", ParagraphStyle(
        name="CoverMeta", parent=styles["BodyText"], alignment=TA_CENTER,
        fontName="Helvetica-Bold", fontSize=10, textColor=colors.HexColor("#0b7285"), spaceAfter=20,
    )))
    story.append(Paragraph(
        "This dossier is a preliminary engineering screen and reviewer handoff. It is not an independent review, professional engineering certification, airworthiness determination, fabrication authorization, or approval to fly.",
        styles["Banner"],
    ))
    cover = Table([
        ["Configuration", "1.40 m span, 4.0 kg target / 4.5 kg maximum concept mass"],
        ["Propulsion", "Two enclosed 70 mm electric ducted fans; 6S 6 Ah conceptual battery"],
        ["Review areas", "Structural loads, flutter, control authority, battery containment, EDF safety"],
        ["Overall disposition", "HOLD - fabrication inputs and qualified independent sign-off required"],
    ], colWidths=[1.35 * inch, 5.6 * inch])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e6f6f8")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#0b5563")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, -1), (1, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (1, -1), (1, -1), colors.HexColor("#b42318")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#b8c4ce")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("LEADING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(cover)
    story.append(PageBreak())

    story.append(Paragraph("1. Executive disposition", styles["Section"]))
    story.append(Paragraph(
        "None of the five review areas can receive a fabrication pass from the current conceptual dataset. The aerodynamic baseline is useful for requirements definition, but it does not contain the material allowables, structural section properties, stiffness and mass distribution, control-surface geometry, actuator data, battery construction, or exact EDF/ESC specifications needed for verification.",
        styles["BodyX"],
    ))
    status_rows = [
        ["Area", "Status", "Reason"],
        ["Structural loads", "BLOCKED", "Load requirement estimated; no spar, skin, joint, or material capacity data."],
        ["Flutter", "BLOCKED", "No modal frequencies, torsional stiffness, hinge free-play, or mass-balance data."],
        ["Control authority", "BLOCKED", "No elevon dimensions, hinge moment, servo torque/speed, or 6-DOF response."],
        ["Battery containment", "BLOCKED", "Pack model, chemistry details, current limits, tray, venting, fuse, and restraint undefined."],
        ["EDF safety", "BLOCKED", "Fan/ESC models, rotor certification, duct clearances, guards, current and temperature tests undefined."],
    ]
    table = Table(status_rows, colWidths=[1.25 * inch, 0.95 * inch, 4.75 * inch], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#102a43")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (1, 1), (1, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (1, 1), (1, -1), colors.HexColor("#b42318")),
        ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#aab7c4")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.2),
        ("LEADING", (0, 0), (-1, -1), 10.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f7fa")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(table)
    story.append(Spacer(1, 10))
    story.append(Paragraph("Decision: DO NOT FABRICATE FROM VERSION 0.2.", styles["Banner"]))

    story.append(Paragraph("2. Structural-load screening", styles["Section"]))
    story.append(Paragraph(
        "For requirements screening only, the maximum concept mass is evaluated at +3.5 g limit load with a 1.5 ultimate factor. Using a simplified spanwise lift resultant at 42% of each semispan gives the following preliminary demand. These values are not a structural capacity calculation and do not address negative-g, landing, launch, gust, concentrated EDF, battery, or control-surface loads.",
        styles["BodyX"],
    ))
    calc_rows = [
        ["Quantity", "Screening value"],
        ["Maximum concept mass", f"{calc['maximum_mass_kg']:.2f} kg"],
        ["Positive limit load", f"+{calc['positive_limit_load_g']:.2f} g"],
        ["Ultimate load factor", f"{calc['positive_ultimate_load_g']:.2f} g"],
        ["Ultimate total lift", f"{calc['ultimate_total_lift_n']:.1f} N"],
        ["Preliminary root moment, each side", f"{calc['preliminary_root_bending_moment_each_side_nm']:.1f} N m"],
    ]
    t = Table(calc_rows, colWidths=[3.6 * inch, 2.0 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0b7285")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#b8c4ce")),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f7fa")]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Paragraph("Required closure evidence", styles["Sub"]))
    story.append(Paragraph(
        "Final mass and CG table; spar geometry and section properties; material allowables and manufacturing process; joint and fastener details; skin/core properties; EDF and battery hard-point loads; positive/negative maneuver, gust, landing and handling cases; finite-element or validated hand analysis; proof-load procedure; and acceptance criteria with no permanent deformation.",
        styles["BodyX"],
    ))

    story.append(Paragraph("3. Flutter and aeroelastic screening", styles["Section"]))
    story.append(Paragraph(
        "No flutter speed can be calculated responsibly from the current model. A flying wing with broad elevons is sensitive to torsional flexibility, hinge free-play and control-surface mass distribution. A speed cap selected without those measurements would be arbitrary.",
        styles["BodyX"],
    ))
    story.append(Paragraph(
        "Required closure evidence: measured wing bending and torsional stiffness; component mass distribution and inertias; elevon hinge stiffness/free-play; actuator compliance; ground-vibration or modal test; control-surface balance assessment; and an aeroelastic analysis demonstrating adequate separation between the approved flight envelope and predicted flutter boundary. Any unexplained buzz, oscillation or control reversal is an immediate stop condition.",
        styles["BodyX"],
    ))

    story.append(Paragraph("4. Control-authority screening", styles["Section"]))
    story.append(Paragraph(
        "The 7% estimated static margin is a reasonable analysis target, but stability margin alone does not prove controllability. Pitch trim, roll rate, stall recovery, asymmetric-thrust response and landing flare authority require defined elevon geometry, aerodynamic derivatives and actuator performance.",
        styles["BodyX"],
    ))
    story.append(Paragraph(
        "Required closure evidence: elevon span/chord and travel limits; hinge-moment estimate across the envelope; servo continuous/stall torque and speed at minimum bus voltage; linkage stiffness and backlash; control allocation and saturation logic; six-degree-of-freedom simulation; hardware-in-the-loop failsafe tests; and reduced-mass glide-article evidence before powered flight.",
        styles["BodyX"],
    ))

    story.append(PageBreak())
    story.append(Paragraph("5. Battery-containment screening", styles["Section"]))
    story.append(Paragraph(
        f"The conceptual 6S 6 Ah pack stores approximately {calc['battery_nominal_energy_wh']:.1f} Wh nominally. The configuration does not yet identify pack construction, maximum continuous current, connector rating, fuse, restraint, impact protection, cooling or a safe vent path. Containment cannot be approved.",
        styles["BodyX"],
    ))
    battery_rows = [
        ["Required feature", "Acceptance evidence"],
        ["Mechanical restraint", "Positive retention in all axes; no reliance on hook-and-loop material alone; reviewed crash-load path."],
        ["Electrical isolation", "Insulated terminals, keyed connector, accessible arming plug and appropriately selected overcurrent protection."],
        ["Thermal protection", "Temperature sensing, conservative current limit, cooling analysis and ground test at worst expected load."],
        ["Failure management", "Vent path away from occupants/electronics, fire-resistant local barrier, damaged-pack quarantine procedure."],
        ["Operations", "Charging outside aircraft with compatible balance charger; storage-state and preflight inspection records."],
    ]
    t = Table(battery_rows, colWidths=[1.45 * inch, 5.55 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#102a43")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#aab7c4")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.4),
        ("LEADING", (0, 0), (-1, -1), 10.8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f7fa")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)

    story.append(Paragraph("6. EDF safety screening", styles["Section"]))
    story.append(Paragraph(
        "The airframe currently specifies only diameter and aggregate conceptual thrust. Rotor integrity, duct clearances, inlet access, foreign-object ingestion, ESC protection and thermal behavior are unresolved.",
        styles["BodyX"],
    ))
    edf_rows = [
        ["Hazard", "Required control before powered testing"],
        ["Rotor burst", "Use manufacturer-rated fan/rotor; inspect and balance; document maximum RPM; provide appropriate local shielding."],
        ["Ingestion/contact", "Guard accessible inlets during ground work; defined exclusion zone; restraints rated above measured static thrust."],
        ["Foreign objects", "Clean duct and work area; tool and fastener accountability; intake inspection before every run."],
        ["Electrical overload", "Matched motor/ESC/battery; logged current and voltage; fuse or equivalent protection; conservative software limit."],
        ["Overtemperature", "Instrument motor, ESC and battery; staged-duration test; automatic abort threshold and cooldown procedure."],
        ["Asymmetric thrust", "Independent shutdown logic and controllability analysis; first flight remains manually commanded and conservative."],
    ]
    t = Table(edf_rows, colWidths=[1.35 * inch, 5.65 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#102a43")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#aab7c4")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.4),
        ("LEADING", (0, 0), (-1, -1), 10.8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f7fa")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)

    story.append(Paragraph("7. Independent-review package required", styles["Section"]))
    story.append(Paragraph(
        "Provide the independent reviewer with the revision-controlled CAD, final bill of materials, mass/CG table, structural substantiation, aeroelastic model and test data, control-system model, component data sheets, wiring/protection diagram, hazard analysis, operating limitations and staged test cards. The reviewer must be free to reject assumptions and request redesign or additional testing.",
        styles["BodyX"],
    ))
    signoff_rows = [
        ["Independent reviewer name", ""],
        ["Qualifications / license / relevant experience", ""],
        ["Organization and independence statement", ""],
        ["Documents and revisions reviewed", ""],
        ["Disposition", "REJECT / REVISE AND RESUBMIT / APPROVE FOR SPECIFIED FABRICATION ONLY"],
        ["Limitations and conditions", ""],
        ["Signature and date", ""],
    ]
    t = Table(signoff_rows, colWidths=[2.35 * inch, 4.65 * inch], rowHeights=[0.42*inch,0.58*inch,0.55*inch,0.55*inch,0.52*inch,0.72*inch,0.55*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e6f6f8")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#7b8794")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.2),
        ("LEADING", (0, 0), (-1, -1), 10.5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "Current project disposition: HOLD. This page is intentionally unsigned. No statement elsewhere in this dossier overrides that status.",
        styles["Banner"],
    ))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def main() -> None:
    config = json.loads((ROOT / "config.json").read_text())
    calc = calculations(config)
    (ROOT / "review" / "screening_calculations.json").write_text(json.dumps(calc, indent=2) + "\n")
    build_pdf(config, calc)
    print(OUTPUT)


if __name__ == "__main__":
    main()
