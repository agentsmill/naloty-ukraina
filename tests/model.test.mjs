import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import {DAY,dim,normalizeDaily,dailyMonths,cumulativeAt,flightState,buildSalvo} from '../js/model.mjs';

const root = new URL('../', import.meta.url);
const html = readFileSync(new URL('index.html', root), 'utf8');
const daily = JSON.parse(readFileSync(new URL('data/daily.json', root), 'utf8'));
const eventCode = html.slice(html.indexOf('const EV=['), html.indexOf('EV.sort('));
const events = vm.runInNewContext(eventCode+'; EV');
const route = (src, city, drone) => ({src, city, drone, durH:drone?5:1});
const mainD = [route('east','central',true)], mainM = [route('sea','central',false)];

test('validates, sorts and deduplicates daily data, including a feed shorter than 30 days', () => {
  const rows=normalizeDaily([{d:'2026-09-02',uav:2,id:3},{d:'2026-09-01',uav:10,id:1},
    {d:'2026-09-01',uav:8,id:2},{d:'2026-02-30',uav:100},{d:'2027-01-01',uav:100},
    {d:'2026-09-03',uav:-1},{d:'2026-09-04',uav:'7'}], '2026-09-18');
  assert.deepEqual(rows.map(r=>r.uav),[8,2]);
});

test('missing dates stay missing; month totals are neither projected nor treated as full', () => {
  const rows=normalizeDaily([{d:'2026-09-01',uav:10},{d:'2026-09-17',uav:20}]);
  const series=dailyMonths(rows,'2026-08-01');
  assert.deepEqual(series,[[2026,9,30,true,2]]);
  assert.equal(cumulativeAt(Date.parse('2026-09-02'),series,rows,'2026-08-01'),10);
  assert.equal(cumulativeAt(Date.parse('2026-09-17'),series,rows,'2026-08-01'),30);
});

test('monthly interpolation uses February and leap years correctly', () => {
  assert.equal(dim(2024,2),29);
  const series=[[2024,2,290,true]];
  assert.equal(cumulativeAt(Date.parse('2024-02-15')+DAY/2,series,null,'2026-08-01'),145);
  assert.equal(cumulativeAt(Date.parse('2024-03-01'),series,null,'2026-08-01'),290);
});

test('daily records are not counted twice with their monthly aggregate', () => {
  const series=[[2026,7,4891,true],...dailyMonths(daily,'2026-08-01')];
  const total=cumulativeAt(Date.parse('2026-09-17T23:59:59Z'),series,daily,'2026-08-01');
  assert.equal(total,4891+4620+2842);
  assert.equal(cumulativeAt(Date.parse('2026-07-01'),series,daily,'2026-08-01'),0);
});

test('flights terminate at arrival, or the exact interception point', () => {
  assert.deepEqual(flightState(4,4),{progress:1,done:true});
  assert.deepEqual(flightState(5,4),{progress:1,done:true});
  assert.deepEqual(flightState(2,4,.5),{progress:.5,done:true});
  assert.deepEqual(flightState(1,4),{progress:.25,done:false});
});

const poolCode=html.slice(html.indexOf('function stepPool('),html.indexOf('/* ══════════════ 6. POST'));
function poolHarness(flight){
  const state={flightState,HRATE:()=>1,ZERO:{},pt:{x:0,y:0,z:0},tan:{x:1,y:0,z:0},
    nightHit:0,nightInt:0,impacts:0,intercepts:0,lastPoint:null,
    dummy:{position:{copy(){}},lookAt(){},scale:{setScalar(){}},updateMatrix(){},rotateZ(){},matrix:{}},
    impact:()=>state.impacts++,intercept:()=>state.intercepts++};
  const r={durH:2,end:{},curve:{getPointAt:t=>state.lastPoint=t,getTangentAt(){}}};
  state.P={n:1,pool:[{on:true,r,t:0,elapsed:0,at:3,evt:true,stop:1,west:false,kind:'m',weight:1,s:1,...flight}],
    mesh:{setMatrixAt(){},instanceMatrix:{}},extra:null};
  vm.createContext(state);vm.runInContext(poolCode,state);return state;
}

test('actual pool uses scheduled launch time, then removes the missile once at arrival',()=>{
  const s=poolHarness();s.stepPool(s.P,1,4,0);
  assert.equal(s.P.pool[0].t,.5);assert.equal(s.lastPoint,.5);
  s.stepPool(s.P,1,5,0);assert.equal(s.P.pool[0].on,false);assert.equal(s.impacts,1);
  s.stepPool(s.P,1,8,0);assert.equal(s.impacts,1);assert.equal(s.nightHit,0);
});

test('west count depends on destination group, not missile model',()=>{
  const s=poolHarness({west:true});s.stepPool(s.P,1,5,0);assert.equal(s.nightHit,1);
  const national=poolHarness();national.stepPool(national.P,1,5,0);assert.equal(national.nightHit,0);
});

test('a long frame intercepts at the specified point without overshoot',()=>{
  const s=poolHarness({west:true,stop:.5});s.stepPool(s.P,1,10,0);
  assert.equal(s.lastPoint,.5);assert.equal(s.intercepts,1);assert.equal(s.nightInt,1);assert.equal(s.impacts,0);
});

test('every event preserves national counts and west weights, including incomplete groups of five', () => {
  for(const e of events){
    const s=buildSalvo(e,route,mainD,mainM);
    assert.equal(s.queue.filter(q=>q.kind!=='m').reduce((n,q)=>n+q.weight,0),e.nat.d,e.d);
    assert.equal(s.queue.filter(q=>q.kind==='m').reduce((n,q)=>n+q.weight,0),e.nat.m,e.d);
    assert.equal(s.queue.filter(q=>q.west).reduce((n,q)=>n+q.weight,0),s.westN,e.d);
    assert.ok(s.queue.every(q=>flightState(s.endH-q.at,q.r.durH,q.stop).done));
  }
});

test('replay is deterministic and the 2023 attack has exactly seven interceptions', () => {
  const e=events.find(e=>e.d==='2023-07-06');
  const first=buildSalvo(e,route,mainD,mainM),again=buildSalvo(e,route,mainD,mainM);
  assert.deepEqual(first,again);
  assert.equal(first.queue.filter(q=>q.stop<1).length,7);
  assert.equal(first.queue.filter(q=>q.west&&q.stop===1).length,3);
});

// Exercise the actual frame coordinator without WebGL, with boundary effects recorded.
const advanceCode=html.slice(html.indexOf('function advancePlayback(dt)'),html.indexOf('function loop(now)'));
function clockHarness(overrides={}){
  const state={playing:true,night:null,ending:false,finished:false,day:0,speed:3,SPAN:10,EV:[],lastEv:-1,lastInc:-1,INC:[],queue:[],
    PD:{},PM:{},motionTime:0,fxLive:[],sLife:[],heatFadeT:0,flowMats:[],waterN:{offset:{x:0,y:0}},
    HRATE:()=>1,rateAt:()=>100,spawn:()=>{state.emitted++;return true;},emitted:0,steps:0,hud:0,
    mainRoutes:[{}],stepPool:()=>state.steps++,stepFx:()=>{},stepSparks:()=>{},heatFade:()=>{},
    liveFlights:()=>state.active,liveEventFlights:()=>state.active,active:false,
    finishPlayback:()=>{state.finished=true;state.playing=false;state.ending=false;},
    clearRoutes:()=>{},fl:{classList:{remove(){}}},updateHUD:()=>state.hud++,
    startNight:i=>{state.lastEv=i;state.day=state.EV[i].f*state.SPAN;state.night={h:0,endH:5,startDay:state.day};},...overrides};
  vm.createContext(state);vm.runInContext(advanceCode,state);return state;
}

test('pause freezes time, emissions, flights and effects', () => {
  const s=clockHarness({playing:false});s.advancePlayback(1);
  assert.equal(s.day,0);assert.equal(s.emitted,0);assert.equal(s.steps,0);assert.equal(s.motionTime,0);
});

test('end drains existing flights and effects, then stops without new launches', () => {
  const s=clockHarness({day:9.9,active:true});s.advancePlayback(.1);
  assert.equal(s.day,10);assert.equal(s.ending,true);assert.equal(s.finished,false);assert.equal(s.emitted,0);
  s.active=false;s.fxLive.push({});s.advancePlayback(.1);assert.equal(s.finished,false);
  s.fxLive=[];s.advancePlayback(.1);assert.equal(s.finished,true);assert.equal(s.playing,false);
  s.advancePlayback(100);assert.equal(s.emitted,0);
});

test('night survives its nominal duration while a flight remains active', () => {
  const s=clockHarness({night:{h:4.9,endH:5,startDay:0,settle:0},active:true});
  s.advancePlayback(2);assert.ok(s.night);assert.equal(s.night.h,5);
  s.active=false;s.advancePlayback(1);assert.ok(s.night);
  s.advancePlayback(1);assert.equal(s.night,null);
});

test('a large timeline step stops at the next event instead of advancing past it', () => {
  const s=clockHarness({EV:[{f:.2}]});s.advancePlayback(1);
  assert.equal(s.day,2);assert.ok(s.night);assert.equal(s.lastEv,0);
});
