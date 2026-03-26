Resize solution

`const maxWidth = 800;`
`const scale = maxWidth / img.width;`

`canvas.width = maxWidth;`
`canvas.height = img.height * scale;`
`ctx.drawImage(img, 0, 0, canvas.width, canvas.height);`