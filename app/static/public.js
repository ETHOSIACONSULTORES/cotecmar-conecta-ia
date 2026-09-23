const $=s=>document.querySelector(s);
const toast=(msg,err=false)=>{const t=$('#toast');t.textContent=msg;t.className='toast show'+(err?' error':'');setTimeout(()=>t.className='toast',3200)};
let eventCode='';
const submitBtn=$('#submitBtn');
const form=$('#providerForm');
const modal=$('#successModal');
const finishBtn=$('#finishBtn');

function resetRegistrationUI(){
  if(modal) modal.style.display='none';
  form.reset();
  $('#eventCode').value=eventCode;
  $('#fileName').textContent='Ningún archivo seleccionado';
  $('#reference').textContent='';
  submitBtn.disabled=false;
  submitBtn.innerHTML='Enviar información <span>→</span>';
  window.scrollTo({top:0,behavior:'smooth'});
}

if(modal) modal.style.display='none';
if(finishBtn) finishBtn.addEventListener('click',e=>{e.preventDefault();resetRegistrationUI();});

async function loadEvent(){
  const qs=new URLSearchParams(location.search); const code=qs.get('event');
  const r=await fetch('/api/public/event'+(code?'?code='+encodeURIComponent(code):''));
  if(!r.ok){$('#eventName').textContent='Evento no disponible';$('#eventMeta').textContent='Solicite un nuevo código QR a COTECMAR';submitBtn.disabled=true;return;}
  const d=await r.json(); eventCode=d.code; $('#eventCode').value=d.code; $('#eventName').textContent=d.name;
  const bits=[d.city,d.venue,d.date?new Date(d.date+'T12:00:00').toLocaleDateString('es-CO',{day:'numeric',month:'long',year:'numeric'}):''].filter(Boolean);
  $('#eventMeta').textContent=bits.join(' · ');
}

const input=$('#documentInput'), zone=$('#uploadZone');
input.addEventListener('change',()=>{$('#fileName').textContent=input.files[0]?.name||'Ningún archivo seleccionado'});
['dragenter','dragover'].forEach(x=>zone.addEventListener(x,e=>{e.preventDefault();zone.classList.add('drag')}));
['dragleave','drop'].forEach(x=>zone.addEventListener(x,e=>{e.preventDefault();zone.classList.remove('drag')}));
zone.addEventListener('drop',e=>{if(e.dataTransfer.files.length){input.files=e.dataTransfer.files;$('#fileName').textContent=input.files[0].name}});

form.addEventListener('submit',async e=>{
  e.preventDefault();
  if(!eventCode){toast('No hay un evento activo.',true);return;}
  submitBtn.disabled=true; submitBtn.innerHTML='<span class="spinner"></span> Procesando información…';
  try{
    const fd=new FormData(e.currentTarget);
    const r=await fetch('/api/providers',{method:'POST',body:fd});
    const d=await r.json();
    if(!r.ok) throw new Error(d.detail||'No fue posible registrar la información');
    $('#reference').textContent='Referencia de registro: PRV-'+String(d.provider_id).padStart(5,'0');
    if(modal) modal.style.display='grid';
    submitBtn.disabled=false;
    submitBtn.innerHTML='Enviar información <span>→</span>';
  }catch(err){
    toast(err.message,true);
    submitBtn.disabled=false;
    submitBtn.innerHTML='Enviar información <span>→</span>';
  }
});

loadEvent().catch(()=>toast('No fue posible cargar la información del evento.',true));
