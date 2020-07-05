var postFile = {
    init: function () {
        var t = this;
        t.regional = document.getElementById('label');
        t.getImage = document.getElementById('get_image');
        t.editPic = document.getElementById('edit_pic');
        t.editBox = document.getElementById('cover_box');
        t.px = 0;
        t.py = 0;
        t.sx = 15;
        t.sy = 15;
        t.sHeight = 150;
        t.sWidth = 150;
        document.getElementById('post_file').addEventListener("change", t.handleFiles, false);
    },
}
handleFiles: function () {
    var fileList = this.files[0];
    var oFReader = new FileReader();
    oFReader.readAsDataURL(fileList);
    oFReader.onload = function (oFREvent) {
        postFile.paintImage(oFREvent.target.result);
    };
},
paintImage: function (url) {
    var t = this;
    var createCanvas = t.getImage.getContext("2d");
    var img = new Image();
    img.src = url;
    img.onload = function () {
        if (img.width < t.regional.offsetWidth && img.height < t.regional.offsetHeight) {
            t.imgWidth = img.width;
            t.imgHeight = img.height;
        } else {
            var pWidth = img.width / (img.height / t.regional.offsetHeight);
            var pHeight = img.height / (img.width / t.regional.offsetWidth);
            t.imgWidth = img.width > img.height ? t.regional.offsetWidth : pWidth;
            t.imgHeight = img.height > img.width ? t.regional.offsetHeight : pHeight;
        }
        t.px = (t.regional.offsetWidth - t.imgWidth) / 2 + 'px';
        t.py = (t.regional.offsetHeight - t.imgHeight) / 2 + 'px';

        t.getImage.height = t.imgHeight;
        t.getImage.width = t.imgWidth;
        t.getImage.style.left = t.px;
        t.getImage.style.top = t.py;

        createCanvas.drawImage(img, 0, 0, t.imgWidth, t.imgHeight);
        t.imgRrl = t.getImage.toDataURL();
        t.cutImage();
        t.drag();
    };
},
drag: function () {
    var t = this;
    
}
