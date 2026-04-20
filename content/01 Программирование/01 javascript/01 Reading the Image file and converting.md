#### 1. Reading the Image File

javascript

```
const file = fileInput.files[0];
const reader = new FileReader();
reader.onload = function(event) {
  const img = new Image();
  img.onload = function() {
    // Process image here
  };
  img.src = event.target.result;
};
reader.readAsDataURL(file);
```

Converting

```
const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d");

canvas.width = img.width;
canvas.height = img.height;

ctx.drawImage(img, 0, 0);

const converted = canvas.toDataURL(format); // PNG, JPEG, or WebP
```
```
```

Download

```
link.href = converted;
link.download = "converted-image";
link.style.display = "inline";
```