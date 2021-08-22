class Foto {
    constructor() {
        var t = this;
        this.operationOrgCanvas = document.createElement("canvas"), this.operationOrgCtx = this.operationOrgCanvas.getContext("2d"), this.operationEditedCanvas = document.createElement("canvas"), this.operationEditedCtx = this.operationEditedCanvas.getContext("2d"), this.fileInput = document.getElementById("foto-file"), this.fileInput.addEventListener("change", function(e) { t.loadImage() }), this.image = null, this.imageData = null, this.imageWidth = 0, this.imageHeight = 0, this.convertedToGrayScale = !1, this.previewImageElement = null, this.redPixelMatrix = [], this.greenPixelMatrix = [], this.bluePixelMatrix = [], this.alphaPixelMatrix = [], this.pickedR = "", this.pickedG = "", this.pickedB = "", this.selectedFileName = "", this.selectStart = !1, this.startX = "", this.startY = "", this.endX = "", this.endY = "", this.excludeArea = !1, this.relativeStartX = "", this.relativeStartY = "", this.relativeEndX = "", this.relativeEndY = "", this.pickedR = null, this.pickedG = null, this.pickedB = null, this.selectRect = document.createElement("div"), document.body.appendChild(this.selectRect), this.oldSelectedColorForColorize = null, this.ctrlPressed = !1;
        t = this;
        document.addEventListener("keydown", function(e) { 17 == e.keyCode && (t.ctrlPressed = !0) }), document.addEventListener("keyup", function(e) { t.ctrlPressed = !0 })
    }
    loadImage() {
        var t = document.getElementById("foto-file");
        this.selectedFileName = t.files.item(0).name;
        var e = new FileReader,
            a = this;
        e.onload = function(t) { a.image = new Image, a.image.onload = function() { a.imageWidth = a.image.width, a.imageHeight = a.image.height, a.operationOrgCanvas.width = a.imageWidth, a.operationOrgCanvas.height = a.imageHeight, a.operationEditedCanvas.width = a.imageWidth, a.operationEditedCanvas.height = a.imageHeight, a.imageData = [], a.operationOrgCtx.clearRect(0, 0, a.operationOrgCanvas.width, a.operationOrgCanvas.height), a.operationEditedCtx.clearRect(0, 0, a.operationEditedCanvas.width, a.operationEditedCanvas.height), a.operationOrgCtx.drawImage(a.image, 0, 0), a.operationEditedCtx.drawImage(a.image, 0, 0), a.previewImage(a.operationOrgCanvas, 0), a.imageData = a.operationOrgCtx.getImageData(0, 0, a.operationOrgCanvas.width, a.operationOrgCanvas.height), a.generatePixelMatrix(), console.log("Pixel Data Loaded") }, a.image.src = t.target.result }, e.readAsDataURL(t.files[0])
    }
    generatePixelMatrix() {
        var t = [],
            e = [],
            a = [],
            i = [];
        this.redPixelMatrix = [], this.greenPixelMatrix = [], this.bluePixelMatrix = [], this.alphaPixelMatrix = [];
        for (var r = 0; r < this.imageData.data.length; r += 4) r / 4 % this.imageWidth == 0 && (0 != r && (this.redPixelMatrix.push(t), this.greenPixelMatrix.push(e), this.bluePixelMatrix.push(a), this.alphaPixelMatrix.push(i)), t = [], e = [], a = [], i = []), t.push(this.imageData.data[r]), e.push(this.imageData.data[r + 1]), a.push(this.imageData.data[r + 2]), i.push(this.imageData.data[r + 3])
    }
    grayscale() {
        for (var t = this.imageData, e = 0; e < t.data.length; e += 4) {
            var a = t.data[e],
                i = t.data[e + 1],
                r = t.data[e + 2];
            t.data[e + 3];
            t.data[e] = (a + i + r) / 3, t.data[e + 1] = (a + i + r) / 3, t.data[e + 2] = (a + i + r) / 3
        }
        this.operationEditedCtx.putImageData(t, 0, 0), this.operationOrgCtx.putImageData(t, 0, 0), this.previewImage(), this.convertedToGrayScale = !this.convertedToGrayScale
    }
    makeBright() {
        for (var t = this.imageData, e = 0; e < t.data.length; e += 4) {
            var a = t.data[e],
                i = t.data[e + 1],
                r = t.data[e + 2],
                s = t.data[e + 3];
            t.data[e] = a + 10, t.data[e + 1] = i + 10, t.data[e + 2] = r + 10, t.data[e + 3] = s
        }
        this.operationEditedCtx.putImageData(t, 0, 0), this.previewImage()
    }
    makeDark() {
        for (var t = this.imageData, e = 0; e < t.data.length; e += 4) t.data[e] -= 10, t.data[e + 1] -= 10, t.data[e + 2] -= 10, t.data[e + 3] -= 10;
        this.operationEditedCtx.putImageData(t, 0, 0), this.previewImage()
    }
    makeTransparent() {
        for (var t = this.imageData, e = 0; e < t.data.length; e += 4) Math.abs(t.data[e] - this.pickedR) < 30 && Math.abs(t.data[e + 1] - this.pickedG) < 30 && Math.abs(t.data[e + 2] - this.pickedB) < 30 && (t.data[e + 3] = 0);
        this.operationEditedCtx.putImageData(t, 0, 0), this.previewImage()
    }
    applyFilter(t) {
        for (var e = 0; e < this.imageData.data.length; e += 4) {
            var a = parseInt(e / 4 / this.imageWidth),
                i = e / 4 % this.imageWidth;
            if (0 != a && 0 != i && a != this.imageHeight - 1 && i != this.imageWidth - 1) {
                for (var r = 0, s = 0, h = 0, o = 0, d = 0; d < 3; d++)
                    for (var n = 0; n < 3; n++) null != this.redPixelMatrix[a + (d - 1)] && null != this.redPixelMatrix[a + (d - 1)][i + (n - 1)] && (r += t[d][n] * this.redPixelMatrix[a + (d - 1)][i + (n - 1)], s += t[d][n] * this.greenPixelMatrix[a + (d - 1)][i + (n - 1)], h += t[d][n] * this.bluePixelMatrix[a + (d - 1)][i + (n - 1)], o += t[d][n] * this.alphaPixelMatrix[a + (d - 1)][i + (n - 1)]);
                this.convertedToGrayScale ? (this.imageData.data[e] = (r + s + h) / 3, this.imageData.data[e + 1] = (r + s + h) / 3, this.imageData.data[e + 2] = (r + s + h) / 3, this.imageData.data[e + 3] = o) : (this.imageData.data[e] = r, this.imageData.data[e + 1] = s, this.imageData.data[e + 2] = h, this.imageData.data[e + 3] = o)
            }
        }
        this.operationEditedCtx.putImageData(this.imageData, 0, 0), this.previewImage()
    }
    applyBlurFilter() {
        this.applyFilter([
            [1 / 9, 1 / 9, 1 / 9],
            [1 / 9, 1 / 9, 1 / 9],
            [1 / 9, 1 / 9, 1 / 9]
        ])
    }
    applyEmbossFilter() {
        this.applyFilter([
            [-2, -1, 0],
            [-1, 1, 1],
            [0, 1, 2]
        ])
    }
    applySharpFilter() {
        this.applyFilter([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ])
    }
    applyVintageFilter() { this.colorFilter("#0000ff"), this.colorFilter("#0000ff"), this.colorFilter("#ec8900") }
    applyCustom() {
        this.applyFilter([
            [-1, -1, -1],
            [2, 2, 2],
            [-1, -1, -1]
        ])
    }
    flipVertically() { this.operationEditedCtx.translate(this.imageWidth, 0), this.operationEditedCtx.scale(-1, 1), this.operationEditedCtx.drawImage(this.image, 0, 0), this.operationOrgCtx.translate(this.imageWidth, 0), this.operationOrgCtx.scale(-1, 1), this.operationOrgCtx.drawImage(this.image, 0, 0), this.imageData = this.operationOrgCtx.getImageData(0, 0, this.operationOrgCanvas.width, this.operationOrgCanvas.height), this.generatePixelMatrix(), this.previewImage() }
    flipHorizontally() { this.operationEditedCtx.translate(0, this.imageHeight), this.operationEditedCtx.scale(1, -1), this.operationEditedCtx.drawImage(this.image, 0, 0), this.operationOrgCtx.translate(0, this.imageHeight), this.operationOrgCtx.scale(1, -1), this.operationOrgCtx.drawImage(this.image, 0, 0), this.imageData = this.operationOrgCtx.getImageData(0, 0, this.operationOrgCanvas.width, this.operationOrgCanvas.height), this.generatePixelMatrix(), this.previewImage() }
    rotate(t) { this.operationEditedCtx.clearRect(0, 0, this.operationEditedCanvas.width, this.operationEditedCanvas.height), this.operationEditedCtx.save(), this.operationEditedCtx.translate(this.imageWidth / 2, this.imageHeight / 2), this.operationEditedCtx.rotate(t * Math.PI / 180), this.operationEditedCtx.drawImage(this.image, -this.image.width / 2, -this.image.width / 2), this.operationEditedCtx.restore(), this.operationOrgCtx.clearRect(0, 0, this.operationOrgCanvas.width, this.operationOrgCanvas.height), this.operationOrgCtx.save(), this.operationOrgCtx.translate(this.imageWidth / 2, this.imageHeight / 2), this.operationOrgCtx.rotate(t * Math.PI / 180), this.operationOrgCtx.drawImage(this.image, -this.image.width / 2, -this.image.width / 2), this.operationOrgCtx.restore(), this.imageData = this.operationOrgCtx.getImageData(0, 0, this.operationOrgCanvas.width, this.operationOrgCanvas.height), this.generatePixelMatrix(), this.previewImage() }
    export () {
        var t = document.createElement("a");
        t.download = this.selectedFileName + "-edited.png", t.href = this.operationEditedCanvas.toDataURL(), t.click()
    }
    previewImage(t, e, a) {
        this.previewImageElement = document.getElementById("foto-image"), this.previewImageElement.setAttribute("draggable", !1);
        var i = this;
        null != e && 0 == e && (this.previewImageElement.addEventListener("mouseover", function(t) { this.style.cursor = "crosshair" }), this.previewImageElement.addEventListener("click", function(t) { i.relativeStartX = t.offsetX, i.relativeStartY = t.offsetY, i.ctrlPressed && i.pickColorPixel(i.relativeStartX, i.relativeStartY), i.selectStart = !1 }), this.previewImageElement.addEventListener("mousedown", function(t) { i.selectStart = !0, i.startX = t.clientX, i.startY = t.clientY, i.relativeStartX = t.offsetX, i.relativeStartY = t.offsetY }), this.previewImageElement.addEventListener("mousemove", function(t) { i.endX = t.clientX, i.endY = t.clientY, i.selectStart && (i.selectRect.style.position = "fixed", i.selectRect.style.display = "initial", i.selectRect.style.border = "2px dashed black", i.selectRect.style.top = i.startY + "px", i.selectRect.style.left = i.startX + "px", i.selectRect.style.height = i.endY - i.startY + "px", i.selectRect.style.width = i.endX - i.startX + "px") }), this.previewImageElement.addEventListener("mouseup", function(t) { i.relativeEndX = t.layerX, i.relativeEndY = t.layerY, i.selectStart = !1, i.selectRect.style.height = "0px", i.selectRect.style.width = "0px", i.selectRect.style.display = "none" }), this.selectRect.addEventListener("mouseup", function(t) { i.selectStart = !1 })), this.previewImageElement.src = null == t ? i.operationEditedCanvas.toDataURL() : t.toDataURL()
    }
    recreateImageObject() { this.image = new Image, this.image.src = this.operationOrgCanvas.toDataURL() }
    pickColorPixel(t, e) {
        var a = this.previewImageElement.width,
            i = this.previewImageElement.height,
            r = this.imageWidth / a,
            s = this.imageHeight / i,
            h = parseInt(t * r),
            o = parseInt(e * s),
            d = this.operationOrgCtx.getImageData(h, o, 1, 1).data;
        this.pickedR = d[0], this.pickedG = d[1], this.pickedB = d[2], this.pickedA = d[3], document.getElementById("color-preview").style.background = "rgb(" + this.pickedR + ", " + this.pickedG + ", " + this.pickedB + ")"
    }
    applyColorFilter(t) {
        for (var e = .5 * parseInt(t.substr(1, 2), 16), a = .5 * parseInt(t.substr(3, 2), 16), i = .5 * parseInt(t.substr(5, 2), 16), r = this.imageData, s = 0; s < r.data.length; s += 4) r.data[s] <= e && (r.data[s] = e), r.data[s + 1] <= a && (r.data[s + 1] = a), r.data[s + 2] <= i && (r.data[s + 2] = i);
        this.operationEditedCtx.putImageData(r, 0, 0), this.operationOrgCtx.putImageData(r, 0, 0), this.previewImage()
    }
    colorize(t) {
        var e = .5 * parseInt(t.substr(1, 2), 16),
            a = .5 * parseInt(t.substr(3, 2), 16),
            i = .5 * parseInt(t.substr(5, 2), 16);
        null != this.oldSelectedColorForColorize && (e = -parseInt(this.oldSelectedColorForColorize.substr(1, 2), 16) + e, a = -parseInt(this.oldSelectedColorForColorize.substr(3, 2), 16) + a, i = -parseInt(this.oldSelectedColorForColorize.substr(3, 2), 16) + i), this.oldSelectedColorForColorize = t;
        for (var r = this.imageData, s = 0; s < r.data.length; s += 4) r.data[s] += e, r.data[s + 1] += a, r.data[s + 2] += i;
        this.operationEditedCtx.putImageData(r, 0, 0), this.operationOrgCtx.putImageData(r, 0, 0), this.previewImage()
    }
    cropSelected() {
        var t = this.previewImageElement.width,
            e = this.previewImageElement.height,
            a = this.imageWidth / t,
            i = this.imageHeight / e,
            r = this.relativeStartX * a,
            s = this.relativeStartY * i,
            h = parseInt(parseInt(this.selectRect.style.width.replace(/\D/g, "")) * a),
            o = parseInt(parseInt(this.selectRect.style.height.replace(/\D/g, "")) * i),
            d = this.operationEditedCtx.getImageData(r, s, h, o),
            n = this.operationOrgCtx.getImageData(r, s, h, o);
        this.operationEditedCtx.clearRect(0, 0, this.operationEditedCanvas.width, this.operationEditedCanvas.height), this.operationOrgCtx.clearRect(0, 0, this.operationOrgCtx.width, this.operationOrgCtx.height), this.operationEditedCanvas.width = h, this.operationEditedCanvas.height = o, this.operationOrgCanvas.width = h, this.operationOrgCanvas.height = o, this.operationEditedCtx.putImageData(d, 0, 0), this.operationOrgCtx.putImageData(n, 0, 0), this.imageWidth = h, this.imageHeight = o, this.imageData = this.operationOrgCtx.getImageData(0, 0, this.operationOrgCanvas.width, this.operationOrgCanvas.height), this.generatePixelMatrix(), this.selectRect.style.display = "none", this.previewImage()
    }
}