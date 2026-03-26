### Копировать страницы в pdf

```
javascript:(async function(){

function clean(t){return (t||'').replace(/\s+/g,' ').trim()}

let input=prompt("Введите страницы (пример: 5-12 или 7)","1-3");
if(!input) return;

let start,end;
if(input.includes('-')){
 let p=input.split('-').map(v=>parseInt(v.trim(),10));
 start=p[0]; end=p[1];
}else{
 start=parseInt(input,10);
 end=start;
}

if(!start||!end){alert("Неверный диапазон");return;}
if(end<start){let t=start;start=end;end=t}

let result='';

for(let i=start;i<=end;i++){

 let page=document.querySelector(`.page[data-page-number="${i}"]`);
 if(!page) continue;

 page.scrollIntoView();
 await new Promise(r=>setTimeout(r,250));

 let layer=null;

 for(let k=0;k<25;k++){
  layer=page.querySelector('.textLayer');
  if(layer) break;
  await new Promise(r=>setTimeout(r,120));
 }

 if(!layer) continue;

 const spans=[...layer.querySelectorAll('span')];
 let text='';

 for(const s of spans){
  const t=clean(s.innerText);
  if(t) text+=t+' ';
 }

 text=text.replace(/\s+/g,' ').trim();

 if(text){
  result+=`\n\n--- PAGE ${i} ---\n\n`+text;
 }

}

if(!result){
 alert("Не удалось собрать текст");
 return;
}

/* панель копирования */
const panel=document.createElement("div");
panel.style.cssText="position:fixed;top:20px;right:20px;background:#111;color:#fff;padding:14px;z-index:999999;border-radius:8px;font-size:14px;max-width:300px";

const btn=document.createElement("button");
btn.textContent="Скопировать текст";
btn.style.cssText="margin-top:8px;padding:6px 10px;cursor:pointer";

btn.onclick=async()=>{
 try{
  await navigator.clipboard.writeText(result);
  btn.textContent="Скопировано ✓";
 }catch(e){
  const ta=document.createElement("textarea");
  ta.value=result;
  document.body.appendChild(ta);
  ta.select();
  document.execCommand("copy");
  ta.remove();
  btn.textContent="Скопировано ✓";
 }
};

panel.innerHTML="Текст готов: "+start+"–"+end+" страниц";
panel.appendChild(document.createElement("br"));
panel.appendChild(btn);

document.body.appendChild(panel);

})();
```

### Код для копирования конспекта в Deepseek
```
javascript:(async function(){  const root=[...document.querySelectorAll('.ds-markdown')].pop(); if(!root){alert("ds-markdown not found");return;}  function htmlToText(html){

  /* конвертация таблиц в markdown */
  html = html.replace(/<table[^>]*>[\s\S]*?<\/table>/gi,(table)=>{
    const doc=new DOMParser().parseFromString(table,"text/html");
    const rows=[...doc.querySelectorAll("tr")];
    if(!rows.length) return "";
    let md="\n";
    rows.forEach((tr,i)=>{
      const cells=[...tr.querySelectorAll("th,td")]
        .map(c=>(c.innerText||"").replace(/\n+/g," ").trim());
      md+="| "+cells.join(" | ")+" |\n";
      if(i===0){
        md+="| "+cells.map(()=> "---").join(" | ")+" |\n";
      }
    });
    md+="\n";
    return md;
  });

  return html
  .replace(/<h[2-4][^>]*>(.*?)<\/h[2-4]>/gi,"\n##%20$1\n")
  .replace(/<strong>(.*?)<\/strong>/gi,"**$1**")
  .replace(/<b>(.*?)<\/b>/gi,"**$1**")
  .replace(/<em>(.*?)<\/em>/gi,"*$1*")
  .replace(/<i>(.*?)<\/i>/gi,"*$1*")
  /* ИСПРАВЛЕНЫ СПИСКИ */
  .replace(/<li>\s*<p[^>]*>(.*?)<\/p>\s*<\/li>/gi,"-%20$1\n")
  .replace(/<li>(.*?)<\/li>/gi,"-%20$1\n")
  .replace(/<\/ul>/gi,"\n")
  .replace(/<\/ol>/gi,"\n")
  .replace(/<br\s*\/?>/gi,"\n")
  .replace(/<p[^>]*>/gi,"\n")
  .replace(/<\/p>/gi,"\n")
  .replace(/<[^>]+>/g,"")
  .replace(/\n{3,}/g,"\n\n")
  .trim();
}  /* берём только Источник + Ссылка */  let sourceBlock="";  [...root.querySelectorAll("p")].forEach(p=>{  

const t = (p.innerText || "").trim().toLowerCase();
const words = ["источник", "ссылка", "source", "link"];

if (words.some(w => t.startsWith(w))) {
    sourceBlock += p.outerHTML;
}}); 

 /* секции */  
 
 let sections=[];  const headers=[...root.querySelectorAll("h3,h4")] .filter(h=>/^\d+/.test(h.innerText.trim()));  headers.forEach((h,i)=>{  let html=h.outerHTML;  let el=h.nextElementSibling;   while(el && el!==headers[i+1]){   html+=el.outerHTML;   el=el.nextElementSibling;  }   /* источник в конец */  html+=sourceBlock;   sections.push(html);  });  /* fallback */  

if(!sections.length){  await navigator.clipboard.writeText(htmlToText(root.innerHTML));  alert("%D0%A1%D0%BA%D0%BE%D0%BF%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%20%D0%B2%D0%B5%D1%81%D1%8C%20%D1%82%D0%B5%D0%BA%D1%81%D1%82");  return;}  

/* панель */  let i=0;  const panel=document.createElement("div");  panel.style.cssText="position:fixed;top:20px;right:20px;width:520px;height:80vh;background:white;border:2px%20solid%20black;z-index:999999;padding:10px;display:flex;flex-direction:column;font-family:sans-serif";  const header=document.createElement("div");  header.style.fontWeight="bold";  const view=document.createElement("div");  view.style.cssText="flex:1;overflow:auto;border:1px%20solid%20#ccc;padding:8px;margin-top:6px";  

const btn=document.createElement("button"); 
 btn.innerText="%D0%A1%D0%BB%D0%B5%D0%B4%D1%83%D1%8E%D1%89%D0%B8%D0%B9%20%D0%B1%D0%BB%D0%BE%D0%BA";  btn.style.marginTop="8px";  
 
panel.appendChild(header);  panel.appendChild(view);  panel.appendChild(btn);  document.body.appendChild(panel);  

async function show(){  if(i>=sections.length){  panel.remove();  return;  }   const html=sections[i];  view.innerHTML=html;   const md=htmlToText(html);  await navigator.clipboard.writeText(md);   header.innerText="%D0%A1%D0%BA%D0%BE%D0%BF%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%20%D0%B1%D0%BB%D0%BE%D0%BA%20"+(i+1)+"%20/%20"+sections.length;  }  

btn.onclick=()=>{  i++;  show();  };  show();  })();
```

### Код для ChatGpt
```
javascript:(async function(){

const root=[...document.querySelectorAll('.ds-markdown, .markdown')].pop();
if(!root){alert("message not found");return;}

function tableToMd(table){
const rows=[...table.querySelectorAll("tr")].map(r=>
[...r.querySelectorAll("th,td")].map(c=>c.innerText.trim())
);
if(!rows.length)return "";

let md="";
md+="| "+rows[0].join(" | ")+" |\n";
md+="| "+rows[0].map(()=> "---").join(" | ")+" |\n";

for(let i=1;i<rows.length;i++){
md+="| "+rows[i].join(" | ")+" |\n";
}
return md+"\n";
}

function convertLists(container){

container.querySelectorAll("li").forEach(li=>{
const depth=li.closest("ul,ol")?.parentElement?.closest("li")
? li.closest("ul,ol").parentElement.closest("li").querySelectorAll("ul ul").length
: 0;

const indent="  ".repeat(depth);
const text=li.firstChild?.textContent?.trim()||li.innerText.trim();

const marker=document.createTextNode("\n"+indent+"- "+text+"\n");
li.replaceWith(marker);
});

}

function htmlToText(html){

const div=document.createElement("div");
div.innerHTML=html;

/* списки */
div.querySelectorAll("li p").forEach(p=>{
p.outerHTML=p.innerHTML;
});

convertLists(div);

/* таблицы */
div.querySelectorAll("table").forEach(t=>{
const md=tableToMd(t);
const pre=document.createElement("pre");
pre.innerText=md;
t.replaceWith(pre);
});

let text=div.innerHTML
.replace(/<h[1-4][^>]*>(.*?)<\/h[1-4]>/gi,"\n## $1\n")
.replace(/<strong>(.*?)<\/strong>/gi,"**$1**")
.replace(/<b>(.*?)<\/b>/gi,"**$1**")
.replace(/<em>(.*?)<\/em>/gi,"*$1*")
.replace(/<i>(.*?)<\/i>/gi,"*$1*")

.replace(/<\/ul>/gi,"\n")
.replace(/<\/ol>/gi,"\n")

.replace(/<br\s*\/?>/gi,"\n")
.replace(/<p[^>]*>/gi,"\n")
.replace(/<\/p>/gi,"\n")

.replace(/<[^>]+>/g,"")
.replace(/\n{3,}/g,"\n\n")
.trim();

/* убираем лишние | */
text=text.split("\n").map(line=>{
const pipes=(line.match(/\|/g)||[]).length;
if(pipes>=2) return line;
return line.replace(/\|/g,"");
}).join("\n");

return text;
}

/* источник */
let sourceBlock="";
[...root.querySelectorAll("p")].forEach(p=>{
const t=p.innerText||"";
if(t.includes("Источник")){
sourceBlock=p.outerHTML;
}
});

/* секции */
let sections=[];
const headers=[...root.querySelectorAll("h1,h2,h3,h4")]
.filter(h=>/^\d+/.test(h.innerText.trim()));

headers.forEach((h,i)=>{
let html=h.outerHTML;
let el=h.nextElementSibling;

while(el && el!==headers[i+1]){
html+=el.outerHTML;
el=el.nextElementSibling;
}

html+=sourceBlock;
sections.push(html);
});

/* fallback */
if(!sections.length){
await navigator.clipboard.writeText(htmlToText(root.innerHTML));
alert("Скопирован весь текст");
return;
}

/* UI */
let i=0;

const panel=document.createElement("div");
panel.style.cssText="position:fixed;top:20px;right:20px;width:520px;height:80vh;background:white;border:2px solid black;z-index:999999;padding:10px;display:flex;flex-direction:column;font-family:sans-serif";

const header=document.createElement("div");
header.style.fontWeight="bold";

const view=document.createElement("div");
view.style.cssText="flex:1;overflow:auto;border:1px solid #ccc;padding:8px;margin-top:6px";

const btn=document.createElement("button");
btn.innerText="Следующий блок";
btn.style.marginTop="8px";

panel.appendChild(header);
panel.appendChild(view);
panel.appendChild(btn);
document.body.appendChild(panel);

async function show(){
if(i>=sections.length){
panel.remove();
return;
}

const html=sections[i];
view.innerHTML=html;

const md=htmlToText(html);
await navigator.clipboard.writeText(md);

header.innerText="Скопирован блок "+(i+1)+" / "+sections.length;
}

btn.onclick=()=>{
i++;
show();
};

show();

})();
```