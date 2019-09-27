# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""


from reportlab.lib.colors import cyan, lightgrey
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas as RLCanvas
from reportlab.lib.pagesizes import A0
import matplotlib.pyplot as plt
import qrcode
from PIL import Image

import skextremes as ske
import matplotlib.pyplot as plt

DPI = 300

data = ske.datasets.portpirie()
data_array = data.asarray()
sea_levels = data.fields.sea_level

model = ske.models.engineering.Lieblein(sea_levels)
with plt.xkcd():
    fig, *_ = model.plot_summary()
    fig.savefig("imgs/example01.png", dpi=DPI)

model = ske.models.classic.GEV(sea_levels, fit_method = 'mle', ci = 0.05,
                              ci_method = 'delta')
with plt.xkcd():
    fig, *_ = model.plot_summary()
    fig.savefig("imgs/example02.png", dpi=DPI)

# Header title, name, affiliation
def make_header(title, filename, author, affiliation, width, height):
    "Create the header with the title, author(s), affiliation(s),..."
    with plt.xkcd():
        fig, ax = plt.subplots(figsize=(width, height))
        ax.set_axis_off()
        ax.text(
            0.5, 0.9,
            title,
            fontsize=45,
            horizontalalignment='center',
            verticalalignment='center'
        )
        ax.text(
            0.5, 0.5,
            author,
            color='grey',
            fontsize=36,
            horizontalalignment='center',
            verticalalignment='center'
        )
        ax.text(
            0.5, 0.25,
            affiliation,
            color='dimgrey',
            fontsize=32,
            horizontalalignment='center',
            verticalalignment='center'
        )
        ax.text(
            -0.05, 0.9,
            'Download Poster',
            color='dimgrey',
            fontsize=20,
            horizontalalignment='center',
            verticalalignment='center'
        )
        ax.text(
            -0.1, 0.8,
            'EN Version',
            color='dimgrey',
            fontsize=15,
            horizontalalignment='center',
            verticalalignment='center'
        )
        ax.text(
            0, 0.8,
            'ES Version',
            color='dimgrey',
            fontsize=15,
            horizontalalignment='center',
            verticalalignment='center'
        )
        fig.savefig(filename, dpi=DPI)
        return fig

def make_qr(msg, filename, color="black", bgcolor="white", size=4):
    import qrcode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=1,
    )
    qr.add_data(msg)
    qr.make(fit=True)
    img = qr.make_image(fill_color=color, back_color=bgcolor)
    img.save(filename)
    return img

def make_XKCD_guy(
    filename,
    x=.5,
    y=.85,
    radius=.1,
    quote=None,
    color='k',
    lw=5,
    xytext=(0, 20),
    arm="left"
    ):
    # Stolen from https://alimanfoo.github.io/2016/05/31/matplotlib-xkcd.html
    fig, ax = plt.subplots(figsize=(10, 15))
    ax.set_axis_off()

    # draw the head
    head = plt.Circle((x, y), radius=radius, edgecolor=color, lw=lw,
                      facecolor='none', zorder=10)
    ax.add_patch(head)
    # draw the body
    body = plt.Line2D([x, x], [y-radius, y-(radius * 4)], 
                      color=color, lw=lw, transform=ax.transAxes)
    ax.add_line(body)
    # draw the arms
    if arm == 'left':
        arm1 = plt.Line2D([x, x+(4*radius)], [y-(radius * 1.5), y-(radius)],
                          color=color, lw=lw, transform=ax.transAxes)
        ax.add_line(arm1)
        arm2 = plt.Line2D([x, x-(radius * .8)], [y-(radius * 1.5), y-(radius*5)],
                          color=color, lw=lw, transform=ax.transAxes)
        ax.add_line(arm2)
    if arm == "right":
        arm1 = plt.Line2D([x, x-(4*radius)], [y-(radius * 1.5), y-(radius)],
                          color=color, lw=lw, transform=ax.transAxes)
        ax.add_line(arm1)
        arm2 = plt.Line2D([x, x+(radius * .8)], [y-(radius * 1.5), y-(radius*5)],
                          color=color, lw=lw, transform=ax.transAxes)
        ax.add_line(arm2)
    # draw the legs
    leg1 = plt.Line2D([x, x+(radius)], [y-(radius * 4), y-(radius*8)], 
                      color=color, lw=lw, transform=ax.transAxes)
    ax.add_line(leg1)
    leg2 = plt.Line2D([x, x-(radius*.5)], [y-(radius * 4), y-(radius*8)], 
                      color=color, lw=lw, transform=ax.transAxes)
    ax.add_line(leg2)

    fig.savefig(filename, transparent=True, dpi=DPI)
    return fig

def make_text_box(title, filename, bullet_points, width, height):
    "Create a text box with information,..."
    with plt.xkcd():
        fig, ax = plt.subplots(figsize=(width, height))
        ax.set_axis_off()
        ax.text(
            -0.15, 0.9,
            title,
            fontsize=48,
            horizontalalignment='left',
            verticalalignment='center'
        )
        for i, bp in enumerate(bullet_points):
            hh = 0.9 / len(bullet_points)
            ax.text(
                -0.1, 0.9 - ((i + 1) * hh),
                f'* {bp}',
                color='dimgrey',
                fontsize=30,
                horizontalalignment='left',
                verticalalignment='center'
            )
        fig.savefig(filename, dpi=DPI)
        return fig

def create_code_example(title, filename, explanation, code, width, height):
    with plt.xkcd():
        fig, ax = plt.subplots(figsize=(width, height))
        ax.set_axis_off()
        ax.text(
            -0.1, 0.95,
            title,
            fontsize=40,
            horizontalalignment='left',
            verticalalignment='center'
        )
        ax.text(
            -0.05, 0.82,
            explanation,
            fontsize=30,
            horizontalalignment='left',
            verticalalignment='center'
        )
    for i, c in enumerate(code.split('\n')):
        hh = 0.75 / len(code.split('\n'))
        ax.text(
            0, 0.75 - ((i + 1) * hh),
            c,
            fontsize=15,
            horizontalalignment='left',
            verticalalignment='center'
        )
    fig.savefig(filename, transparent=True, dpi=DPI)
    return fig

def add_code_example(canvas, filename, plot_filename, x, y, width, height):
    canvas.setFillColor(lightgrey)
    canvas.rect(x, y, width, height, fill=1)
    canvas.drawImage(
        filename,
        x,
        20 * inch,
        width=width,
        height=height*0.2,
        mask=[10, 255, 10, 255, 10, 255]
    )
    canvas.drawImage(
        plot_filename,
        x + width * 0.025,
        y * 1.5,
        width=width * 0.95,
        height=height*0.5
    )

#################################
# Create document and its pieces
#################################
# Canvas (PDF)
canvas = RLCanvas("Poster_PyConES2019_ES.pdf",
                  pagesize=A0,
                  bottomup=1)
# PDF bg color
canvas.setFillColor(cyan)
canvas.rect(0, 0, width=A0[0], height=A0[1], fill=1)
# Width and height in inches
w = A0[0] / inch
h = A0[1] / inch
# Create header and add to PDF
title = "Estimacion de valores extremos usando Python y scikit-extremes"
filename = "imgs/headerES.png"
author = "Kiko Correoso"
affiliation = "https://pybonacci.org"
fig = make_header(title, filename, author, affiliation, w * 0.9, 3)
canvas.drawImage(
    filename,
    w * 0.05 * inch,
    h * 0.90 * inch,
    width=w * 0.9 * inch,
    height=3*inch
)
# Add pybonacci logo to PDF
canvas.drawImage(
    'imgs/pybofractal1.png',
    w * 0.85 * inch,
    h * 0.90 * inch,
    width=3 * inch,
    height=3 * inch
)
# Create QR code with the pybonacci page url
make_qr("https://pybonacci.org", "imgs/qr_pybonacci_org.png", size=10)
# Add the QR to the PDF
canvas.drawImage(
    'imgs/qr_pybonacci_org.png',
    w * 0.59 * inch,
    h * 0.915 * inch,
    width=0.5 * inch,
    height=0.5 * inch
)
# Create QR code with the PDF file url (EN)
url = ("https://github.com/kikocorreoso/scikit-extremes/"
       "tree/master/PosterPyConES2019/Poster_PyConES2019_EN.pdf")
make_qr(url, "imgs/qr_poster_pdf_link_EN.png", size=10)
# Add the QR to the PDF
canvas.drawImage(
    'imgs/qr_poster_pdf_link_EN.png',
    w * 0.06 * inch,
    h * 0.90 * inch,
    width=2 * inch,
    height=2 * inch
)
# Create QR code with the PDF file url (ES)
url = ("https://github.com/kikocorreoso/scikit-extremes/"
       "tree/master/PosterPyConES2019/Poster_PyConES2019_ES.pdf")
make_qr(url, "imgs/qr_poster_pdf_link_ES.png", size=10)
# Add the QR to the PDF
canvas.drawImage(
    'imgs/qr_poster_pdf_link_ES.png',
    w * 0.13 * inch,
    h * 0.90 * inch,
    width=2 * inch,
    height=2 * inch
)
# Create a XKCD guy
make_XKCD_guy('imgs/xkcd01.png')
# Add guy to the PDF
canvas.drawImage(
    'imgs/xkcd01.png',
    w * 0.02 * inch,
    h * 0.725 * inch,
    width=7 * inch,
    height=7 * inch,
    mask=[1,255,1,255,1,255]
)
# Create a text box
title = '¿Que es scikit-extremes:'
bullet_points = [
    'Es una mini biblioteca para hacer calculos univariados de valores extremos.',
    ('El objetivo es rellenar el hueco existente en el ecosistema PyData '
     'para hacer estas estimaciones.'),
    'La teoria de valores extremos (EVT) es una disciplina estadistica unica.',
    ('Se desarrollan modelos y tecnicas para describir lo inusual en lugar de '
     'lo usual.'),
    'Se focaliza en la cola de la distribucion.',
    'Principales campos de interes: hidrologia, meteorologia, oceanografia, ingenieria,...'
]
make_text_box(title, 'imgs/text_box01ES.png', bullet_points, 0.75 * w, 5)
# Add text box to the PDF
canvas.drawImage(
    'imgs/text_box01ES.png',
    w * 0.2 * inch,
    h * 0.75 * inch,
    width=0.75 * w * inch,
    height=5 * inch
)
# Create a XKCD guy
make_XKCD_guy('imgs/xkcd02.png', arm='right')
# Add guy to the PDF
canvas.drawImage(
    'imgs/xkcd02.png',
    w * 0.75 * inch,
    h * 0.535 * inch,
    width=7 * inch,
    height=7 * inch,
    mask=[1,255,1,255,1,255]
)
# Create a text box
title = 'Principales atractivos:'
bullet_points = [
    'Se basa en el stack PyData, testeado en mil batallas.',
    'Se incluyen conjuntos de datos para probar o aprender sobre valores extremos.',
    'Capacidades de graficar.',
    'Ajustes basados en distintas tecnicas (MLE, MOM, L-moments,...).',
    'Incluye modelos simples usados en la industria de la ingenieria.',
    ('Metodos para cuantificar calidad del ajuste (intervalos de confianza, '
     'graficos de probabilidad,...).'),
    'Los metodos cientificos usados se encuentran referenciados y probados.',
    'Incluye documentacion.'
]
make_text_box(title, 'imgs/text_box02ES.png', bullet_points, 0.75 * w, 6)
# Add text box to the PDF
canvas.drawImage(
    'imgs/text_box02ES.png',
    w * 0.05 * inch,
    h * 0.55 * inch,
    width=0.75 * w * inch,
    height=7 * inch
)
# Add code example 01
example01 = """import skextremes as ske
import matplotlib.pyplot as plt

data = ske.datasets.portpirie()
data_array = data.asarray()
sea_levels = data.fields.sea_level

model = ske.models.engineering.Lieblein(sea_levels)

fig, *_ = model.plot_summary()
fig.show()"""
create_code_example('Ejemplo 1:',
                    'imgs/example_text01ES.png',
                    'Ajuste de la altura de ola usando el metodo de Lieblein',
                    example01,
                    0.45 * w,
                    5)
add_code_example(
    canvas,
    'imgs/example_text01ES.png',
    'imgs/example01.png',
    w * 0.05 * inch,
    7 * inch,
    w * 0.425 * inch,
    h * 0.35 * inch)
# Add code example 02
example02 = """import skextremes as ske
import matplotlib.pyplot as plt

data = ske.datasets.portpirie()
data_array = data.asarray()
sea_levels = data.fields.sea_level

model = ske.models.classic.GEV(sea_levels, fit_method = 'mle', ci = 0.05,
                              ci_method = 'delta')

fig, *_ = model.plot_summary()
fig.show()"""
create_code_example('Ejemplo 2:',
                    'imgs/example_text02ES.png',
                    'Ajuste de la altura de ola usando la distribucion GEV',
                    example02,
                    0.45 * w,
                    5)
add_code_example(
    canvas,
    'imgs/example_text02ES.png',
    'imgs/example02.png',
    w * 0.525 * inch,
    7 * inch,
    w * 0.425 * inch,
    h * 0.35 * inch)
# Create a text box
title = 'Mas informacion:'
bullet_points = [
    'Guia de usuario: https://scikit-extremes.readthedocs.io/en/latest/User%20guide.html',
    'RTFD: https://scikit-extremes.readthedocs.io/en/latest/index.html',
    'Repositorio: https://github.com/kikocorreoso/scikit-extremes',
    'Twitter: https://twitter.com/pybonacci'
]
make_text_box(title, 'imgs/text_box03ES.png', bullet_points, 0.9 * w, 4)
# Add text box to the PDF
canvas.drawImage(
    'imgs/text_box03ES.png',
    w * 0.05 * inch,
    h * 0.05 * inch,
    width=0.9 * w * inch,
    height=4 * inch
)
canvas.save()
