from PIL import Image, ImageDraw, ImageFont
A='/home/claude/vx-sports-academy/assets/apparel/'; OUT='/home/claude/vx-sports-academy/ig/2026-12-07/'
W,H=1080,1440; BG=(10,10,11); FG=(240,237,232); Q=(125,125,133)
inter=lambda s,w='Bold': ImageFont.truetype(f'/usr/share/fonts/opentype/inter/Inter-{w}.otf',s)
jp=lambda s: ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',s,index=0)
cols=['ink-black','cloud-white','sage-green','powder-blue','mist-lavender','petal-pink']
def prod(c):
    im=Image.open(f'{A}set-front_{c}.webp').convert('RGB'); s=H/im.height
    im=im.resize((round(im.width*s),H)); x=(im.width-W)//2; return im.crop((x,0,x+W,H))
def foot(d):
    f=inter(20,'Medium'); d.text((72,H-80),'THE PRO PERSPECTIVE.',font=f,fill=Q)
    t='@vx.apparel.official'; d.text((W-72-d.textlength(t,font=f),H-80),t,font=f,fill=Q)
# cover
c=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(c)
d.text((72,110),'VX APPAREL',font=inter(26,'SemiBold'),fill=Q)
d.text((72,160),'6 COLORS.',font=inter(120,'Bold'),fill=FG)
d.text((72,310),'あなたは、どの色？',font=jp(54),fill=FG)
tw,th,g=296,390,24; x0=(W-3*tw-2*g)//2; y0=440
for i,col in enumerate(cols):
    t=prod(col); t=t.crop((90,200,W-90,H-150)).resize((tw,th))
    c.paste(t,(x0+(i%3)*(tw+g), y0+(i//3)*(th+g)))
d.text((72,y0+2*th+g+40),'ユニセックス｜Tシャツ・ショーツ・ソックス',font=jp(30),fill=Q)
foot(d); c.save(OUT+'colors-01.jpg',quality=92)
for i,col in enumerate(cols): prod(col).save(OUT+f'colors-0{i+2}.jpg',quality=92)
# end
c=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(c)
d.text((72,300),'PRE-ORDER',font=inter(26,'SemiBold'),fill=Q)
d.text((72,350),'今は、予約受付中。',font=jp(80),fill=FG)
rows=[('3点セット','¥14,300'),('Tシャツ','¥7,700'),('ショーツ','¥6,600'),('ソックス','¥2,200')]
y=560
for a,b in rows:
    d.line((72,y,W-72,y),fill=(42,42,46),width=2)
    d.text((72,y+36),a,font=jp(44),fill=FG); f=inter(52,'SemiBold'); d.text((W-72-d.textlength(b,font=f),y+30),b,font=f,fill=FG); y+=124
d.line((72,y,W-72,y),fill=(42,42,46),width=2)
d.text((72,y+30),'税込',font=jp(28),fill=Q)
d.text((72,y+150),'色とサイズは、プロフィールのリンクから。',font=jp(38),fill=FG)
foot(d); c.save(OUT+'colors-08.jpg',quality=92)
s=[Image.open(OUT+f'colors-0{i}.jpg').resize((270,360)) for i in (1,2,3,8)]
m=Image.new('RGB',(1080,360));[m.paste(x,(k*270,0)) for k,x in enumerate(s)];m.save('/tmp/colors.jpg')
