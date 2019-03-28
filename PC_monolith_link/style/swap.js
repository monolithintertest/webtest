
<!--
function MM_swapImgRestore() { //v3.0
  var i,x,a=document.MM_sr; for(i=0;a&&i<a.length&&(x=a[i])&&x.oSrc;i++) x.src=x.oSrc;
}

function MM_preloadImages() { //v3.0
  var d=document; if(d.images){ if(!d.MM_p) d.MM_p=new Array();
    var i,j=d.MM_p.length,a=MM_preloadImages.arguments; for(i=0; i<a.length; i++)
    if (a[i].indexOf("#")!=0){ d.MM_p[j]=new Image; d.MM_p[j++].src=a[i];}}
}

function MM_swapImage() { //v3.0
  var i,j=0,x,a=MM_swapImage.arguments; document.MM_sr=new Array; for(i=0;i<(a.length-2);i+=3)
   if ((x=MM_findObj(a[i]))!=null){document.MM_sr[j++]=x; if(!x.oSrc) x.oSrc=x.src; x.src=a[i+2];}
}

function MM_findObj(n, d) { //v4.01
  var p,i,x;  if(!d) d=document; if((p=n.indexOf("?"))>0&&parent.frames.length) {
    d=parent.frames[n.substring(p+1)].document; n=n.substring(0,p);}
  if(!(x=d[n])&&d.all) x=d.all[n]; for (i=0;!x&&i<d.forms.length;i++) x=d.forms[i][n];
  for(i=0;!x&&d.layers&&i<d.layers.length;i++) x=MM_findObj(n,d.layers[i].document);
  if(!x && d.getElementById) x=d.getElementById(n); return x;
}
//-->


<!--
var SymRealOnLoad;
var SymRealOnUnload;

function SymOnUnload()
{
//  window.open = SymWinOpen;
  if(SymRealOnUnload != null)
     SymRealOnUnload();
}

function SymOnLoad()
{
  if(SymRealOnLoad != null)
     SymRealOnLoad();
//  window.open = SymRealWinOpen;
  SymRealOnUnload = window.onunload;
  window.onunload = SymOnUnload;
}

SymRealOnLoad = window.onload;
window.onload = SymOnLoad;

//-->

<!--HPB_SCRIPT_ROV_50
//
//  Licensed Materials - Property of IBM
//  5724I83
//  (C) Copyright IBM Corp. 1995, 2004 All Rights Reserved.
//

// HpbImgPreload:
//
function HpbImgPreload()
{
  var appVer=parseInt(navigator.appVersion);
  var isNC=false,isN6=false,isIE=false;
  if (document.all && appVer >= 4) isIE=true; else
    if (document.getElementById && appVer > 4) isN6=true; else
      if (document.layers && appVer >= 4) isNC=true;
  if (isNC||isN6||isIE)
  {
    if (document.images)
    {
      var imgName = HpbImgPreload.arguments[0];
      var cnt;
      swImg[imgName] = new Array;
      for (cnt = 1; cnt < HpbImgPreload.arguments.length; cnt++)
      {
        swImg[imgName][HpbImgPreload.arguments[cnt]] = new Image();
        swImg[imgName][HpbImgPreload.arguments[cnt]].src = HpbImgPreload.arguments[cnt];
      }
    }
  }
}
// HpbImgFind:
//
function HpbImgFind(doc, imgName)
{
  for (var i=0; i < doc.layers.length; i++)
  {
    var img = doc.layers[i].document.images[imgName];
    if (!img) img = HpbImgFind(doc.layers[i], imgName);
    if (img) return img;
  }
  return null;
}
// HpbImgSwap:
//
function HpbImgSwap(imgName, imgSrc)
{
  var appVer=parseInt(navigator.appVersion);
  var isNC=false,isN6=false,isIE=false;
  if (document.all && appVer >= 4) isIE=true; else
    if (document.getElementById && appVer > 4) isN6=true; else
      if (document.layers && appVer >= 4) isNC=true;
  if (isNC||isN6||isIE)
  {
    if (document.images)
    {
      var img = document.images[imgName];
      if (!img) img = HpbImgFind(document, imgName);
      if (img) img.src = imgSrc;
    }
  }
}
var swImg; swImg=new Array;
//-->

