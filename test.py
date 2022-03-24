# 参考文档
# https://github.com/loonghao/photoshop-python-api/
# https://loonghao.github.io/photoshop-python-api/
# https://theiviaxx.github.io/photoshop-docs/index.html
import os
from tempfile import mkdtemp
from photoshop import Session

with Session() as ps:
    # 创建项目,初始化宽高
    doc_ref = ps.app.documents.add(750, 750)
    # 初始化度量单位为像素
    start_ruler_units = ps.app.preferences.rulerUnits
    if start_ruler_units is not ps.Units.Pixels:
        ps.app.preferences.rulerUnits = ps.Units.Pixels

    # 创建一个选区,该选区边界距离画布边界均为offset
    offset = 50
    selBounds1 = (
        (offset, offset),
        (doc_ref.width - offset, offset),
        (doc_ref.width - offset, doc_ref.height - offset),
        (offset, doc_ref.height - offset)
    )
    doc_ref.selection.select(selBounds1)
    doc_ref.selection.deselect()

    # 添加背景
    fillColor = ps.SolidColor()
    fillColor.rgb.red = 255
    fillColor.rgb.green = 110
    fillColor.rgb.blue = 0
    layer = doc_ref.artLayers.add()
    layer.name = "backColor"
    doc_ref.selection.selectAll()
    doc_ref.selection.fill(fillColor)
    doc_ref.selection.deselect()

    # 添加图片作为图层
    desc = ps.ActionDescriptor
    desc.putPath(ps.app.charIDToTypeID("null"), r"C:\Users\hibian\Downloads\(画集・設定資料集) 君の名は。 公式ビジュアルガイド\002_133.jpg")
    event_id = ps.app.charIDToTypeID("Plc ")
    ps.app.executeAction(event_id, desc)

    # 添加png作为图层
    desc = ps.ActionDescriptor
    desc.putPath(ps.app.charIDToTypeID("null"), r"C:\Users\hibian\Pictures\test\cover-white.png")
    ps.app.executeAction(event_id, desc)

    # 添加文字
    text_color = ps.SolidColor()
    text_color.rgb.red = 255
    text_color.rgb.green = 110
    text_color.rgb.blue = 0

    new_text_layer = doc_ref.artLayers.add()
    new_text_layer.kind = ps.LayerKind.TextLayer
    # 不超过18字
    new_text_layer.textItem.contents = "你的名字原画集你的的名字"
    new_text_layer.textItem.position = [375, 635]
    new_text_layer.textItem.size = 50
    new_text_layer.textItem.color = text_color
    # 居中对齐
    new_text_layer.textItem.justification = ps.Justification.Center
    # 加粗
    new_text_layer.textItem.fauxBold = True

    # 第二行文字
    text_layer = doc_ref.artLayers.add()
    text_layer.kind = ps.LayerKind.TextLayer
    # 不超过18字
    text_layer.textItem.contents = "100P             69M"
    text_layer.textItem.position = [375, 710]
    text_layer.textItem.size = 40
    text_layer.textItem.color = text_color
    # 居中对齐
    text_layer.textItem.justification = ps.Justification.Center
    # 加粗
    text_layer.textItem.fauxBold = True

    # 导出为jpg
    options = ps.JPEGSaveOptions(quality=5)
    jpg_file = os.path.join(mkdtemp("pspy-api"), r"C:\Users\hibian\Pictures\test\test.jpg")
    doc_ref.saveAs(jpg_file, options, asCopy=True)
    ps.app.doJavaScript(f'alert("saved")')
