(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["cameraFeed"],{d7ed:function(e,t,n){"use strict";n.r(t);var a=function(){var e=this,t=e.$createElement,n=e._self._c||t;return e.loading?n("div",{staticClass:"tw-flex tw-justify-center tw-items-center page-loading"},[n("v-progress-circular",{attrs:{indeterminate:"",color:"var(--cui-primary)"}})],1):n("div",{staticClass:"tw-w-full mh-100"},[n("div",{staticClass:"tw-h-full tw-flex tw-justify-center tw-items-center"},[n("vue-aspect-ratio",{attrs:{ar:"16:9",width:e.width+"px"}},[n("v-btn",{staticClass:"tw-text-white",staticStyle:{top:"10px"},attrs:{absolute:"",top:"",left:"",fab:"","x-small":"",color:"rgba(0, 0, 0, 0.5)"},on:{click:function(t){return e.$router.push("/cameras/"+e.camera.name)}}},[n("v-icon",{attrs:{size:"20"}},[e._v(e._s(e.icons["mdiChevronLeft"]))])],1),n("VideoCard",{ref:e.camera.name,attrs:{camera:e.camera,stream:"",noLink:"",hideNotifications:""}})],1)],1)])},i=[],r=n("1da1"),o=(n("96cf"),n("b0c0"),n("d3b7"),n("94ed")),c=n("335a"),s=n("4add"),d=n("c413"),u=n("00c2"),m={name:"Camera",components:{VideoCard:d["a"],"vue-aspect-ratio":c["a"]},mixins:[u["a"]],beforeRouteLeave:function(e,t,n){this.loading=!0,n()},data:function(){return{icons:{mdiChevronLeft:o["D"]},camera:{},cols:12,width:1024,loading:!0}},mounted:function(){var e=this;return Object(r["a"])(regeneratorRuntime.mark((function t(){var n,a;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.prev=0,t.next=3,Object(s["b"])(e.$route.params.name);case 3:return n=t.sent,t.next=6,Object(s["c"])(e.$route.params.name);case 6:a=t.sent,n.data.settings=a.data,e.camera=n.data,["resize","orientationchange"].forEach((function(t){window.addEventListener(t,e.onResize)})),e.onResize(),e.loading=!1,t.next=18;break;case 14:t.prev=14,t.t0=t["catch"](0),console.log(t.t0),e.$toast.error(t.t0.message);case 18:case"end":return t.stop()}}),t,null,[[0,14]])})))()},beforeDestroy:function(){var e=this;["resize","orientationchange"].forEach((function(t){window.removeEventListener(t,e.onResize)}))},methods:{onResize:function(){this.width=this.windowWidth()<1024?this.windowWidth()-40:1024},windowHeight:function(){return Math.max(document.documentElement.clientHeight,window.innerHeight)},windowWidth:function(){return window.innerWidth&&document.documentElement.clientWidth?Math.min(window.innerWidth,document.documentElement.clientWidth):window.innerWidth||document.documentElement.clientWidth||document.getElementsByTagName("body")[0].clientWidth}}},l=m,w=n("2877"),h=n("6544"),f=n.n(h),p=n("8336"),v=n("132d"),g=n("490a"),b=Object(w["a"])(l,a,i,!1,null,"5cb185c5",null);t["default"]=b.exports;f()(b,{VBtn:p["a"],VIcon:v["a"],VProgressCircular:g["a"]})}}]);