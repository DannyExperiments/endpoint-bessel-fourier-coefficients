#!/usr/bin/env python3
"""Render a disk autocorrelation and its nonnegative Fourier multiplier."""
from math import acos, cos, pi, sin, sqrt, tau
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BG, CARD, GRID = "#0b1523", "#132338", "#38516a"
INK, TEXT, GOLD, AQUA, SHADE = "#eff8fe", "#bfd3e5", "#ffce79", "#76dfc7", "#274f54"
W,H = 686,446


def font(size,bold=False):
    for root,regular,strong in [
        ("/System/Library/Fonts/Supplemental","Arial.ttf","Arial Bold.ttf"),
        ("/usr/share/fonts/truetype/dejavu","DejaVuSans.ttf","DejaVuSans-Bold.ttf")]:
        p=Path(root)/(strong if bold else regular)
        if p.is_file():
            return ImageFont.truetype(str(p),size)
    raise RuntimeError("Arial or DejaVu Sans is required")


TITLE,BODY,LABEL,SMALL = font(32,True),font(21),font(21,True),font(17)


def spatial(relative_radius):
    return 2/pi*(acos(relative_radius)-relative_radius*sqrt(1-relative_radius**2))


def psi(argument):
    steps=96
    dt=pi/(2*steps)
    integral=1.
    for k in range(1,steps):
        t=k*dt
        integral+=(4 if k%2 else 2)*cos((argument/2)*sin(t))*cos(t)**2
    return (4/pi*dt*integral/3)**2


def surface(draw,radius,theta):
    def project(x,y,z):
        u=x*cos(theta)+y*sin(theta)
        v=-x*sin(theta)+y*cos(theta)
        return 178+204*u, 261+59*v-108*z
    for k in range(6):
        p=k/5-.5
        draw.line((*project(p,-.5,0),*project(p,.5,0)),fill=GRID,width=1)
        draw.line((*project(-.5,p,0),*project(.5,p,0)),fill=GRID,width=1)
    for k in range(1,11):
        t=k/10
        z=spatial(t)
        points=[project(t*radius*cos(j*tau/40),t*radius*sin(j*tau/40),z)
                for j in range(41)]
        draw.line(points,fill=AQUA,width=2)
    for j in range(12):
        angle=j*tau/12
        points=[project(t*radius*cos(angle),t*radius*sin(angle),spatial(t))
                for t in [k/20 for k in range(21)]]
        draw.line(points,fill=AQUA,width=1)
    x,y=project(0,0,1)
    draw.ellipse((x-4,y-4,x+4,y+4),fill=INK)


def frame(i,n):
    power=1+i*3//n
    radius=2.**(-power)
    angle=tau*i/n+.2
    im=Image.new("RGB",(W,H),BG)
    draw=ImageDraw.Draw(im)
    draw.text((26,17),"Narrower bumps reach more modes",fill=INK,font=TITLE)
    draw.text((27,59),"A positive radial kernel and its squared Fourier response",fill=TEXT,font=BODY)
    for card in ((22,95,335,353),(349,95,664,353)):
        draw.rounded_rectangle(card,14,fill=CARD,outline=GRID)
    draw.text((178,111),f"Spatial radius 1/{2**power}",fill=INK,font=LABEL,anchor="mt")
    surface(draw,radius,angle)
    draw.text((178,326),"Height relative to peak",fill=TEXT,font=SMALL,anchor="mt")
    draw.text((506,111),"Nonnegative multiplier",fill=INK,font=LABEL,anchor="mt")
    left, right, top, bottom = 394,638,151,293
    guaranteed=.5/radius
    gt=left+(right-left)*guaranteed/24
    draw.rectangle((left,top,gt,bottom),fill=SHADE)
    draw.line((left,top,left,bottom,right,bottom),fill=TEXT,width=2)
    for y,label in ((top,"1"),((top+bottom)//2,"1/2"),(bottom,"0")):
        draw.text((left-8,y),label,fill=TEXT,font=SMALL,anchor="rm")
    draw.line((left,(top+bottom)//2,right,(top+bottom)//2),fill=GRID,width=2)
    levels=[(left+(right-left)*j/110,bottom-(bottom-top)*psi(radius*24*j/110))
            for j in range(111)]
    draw.line(levels,fill=AQUA,width=3)
    draw.line((gt,top,gt,bottom),fill=GOLD,width=2)
    draw.text((516,325),"Frequency 0 to 24",fill=TEXT,font=SMALL,anchor="mt")
    draw.text((343,373),f"Half-height guaranteed up to frequency {int(guaranteed)}",fill=INK,font=LABEL,anchor="mt")
    draw.text((343,412),"Each dyadic scale covers one block of Bessel zeros.",fill=TEXT,font=BODY,anchor="mt")
    return im


def main():
    frames=[frame(i,42) for i in range(42)]
    sheet=Image.new("RGB",(W*3,H))
    for j,k in enumerate((0,14,28)):
        sheet.paste(frames[k],(W*j,0))
    palette=sheet.quantize(colors=64)
    indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    file=Path(__file__).with_name("dyadic-kernel.gif")
    indexed[0].save(file,save_all=True,append_images=indexed[1:],duration=120,loop=0,optimize=True)
    print(f"{file.name}: {len(frames)} frames, {file.stat().st_size} bytes")


if __name__=="__main__":
    main()
