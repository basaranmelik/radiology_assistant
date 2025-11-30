from graph.state import GraphState
from tools.llm_calls import get_llm, get_routing_chain, get_extraction_chain
from schemas.form_schemas import FormUstBatinBT,FormAltBatinBT,FormToraksBT,FormKontrastToraksBT, FormBeyinBT, FormLomberBT

llm = get_llm()

def node_router(state: GraphState) -> dict:
    ''' Textin hangi form tipine uygun olduğuna karar verir. '''
    print(f"\n--- DÜĞÜM (Hasta: {state['patient_name']}): Router ---")
    
    text_chunk = state.get("text_chunk", "")

    print("DEBUG (Router): Analiz edilecek metin bloğu:")
    print("-------------------------------------------")
    print(text_chunk)
    print("-------------------------------------------")

    if text_chunk.startswith("HATA:") or text_chunk.startswith("ERROR:"):
        return {"form_type": "undefined", "error": text_chunk}
    
    prompt = f"""
    Sen, tıbbi raporları sınıflandırma konusunda uzman bir asistansın.
    Görevin, sana verilen metin bloğunun konusunu analiz edip, aşağıdaki kategorilerden hangisine ait olduğunu belirlemektir.

    Şu adımları izle:
    1. Kategoriye karar verdiğinde formundaki findings kısmının tamamı sana verilen metinde geçmese de eklemelisin çünkü bazı doktorlar normal olan kısımları okumuyorlar, sadece değiştirilmiş yerlerini varsayılan cümlelerin yerine koyarak ver.


    KATEGORİLER:
    - 'ust_batin': Eğer metin ağırlıklı olarak üst batın BT bulguları, raporları veya ilgili terimler içeriyorsa.
    - 'alt_batin': Eğer metin ağırlıklı olarak alt batın BT bulguları, raporları veya ilgili terimler içeriyorsa.
    - 'toraks': Eğer metin ağırlıklı olarak kontrastsız toraks BT bulguları, raporları veya ilgili terimler içeriyorsa.
    - 'kontrast_toraks': Eğer metin ağırlıklı olarak kontrastlı toraks BT bulguları, raporları veya ilgili terimler içeriyorsa.
    - 'ayak_bilek': Eğer metin ağırlıklı olarak ayak bileği BT bulguları, raporları veya ilgili terimler içeriyorsa.
    - 'beyin': Eğer metin ağırlıklı olarak beyin BT bulguları, raporları veya ilgili terimler içeriyorsa.
    - 'lomber': Eğer metin ağırlıklı olarak lomber BT bulguları, raporları veya ilgili terimler içeriyorsa.
    - 'undefined': Eğer metin bu kategorilerden birine girmiyorsa veya tıbbi bir içerik değilse.

    
    METİN:
    ---
    {text_chunk}
    ---
    """
    
    try:
        routing_chain = get_routing_chain(llm)
        result = routing_chain.invoke(prompt)
        form_type = result.form_type
        print(f"Router kararı: {form_type}")
        return {"form_type": form_type}
    except Exception as e:
        print(f"HATA (Router): LLM çağrısı sırasında hata oluştu: {e}")
from graph.state import GraphState
from tools.llm_calls import get_llm, get_routing_chain, get_extraction_chain
from schemas.form_schemas import FormUstBatinBT,FormAltBatinBT,FormToraksBT,FormKontrastToraksBT, FormBeyinBT, FormLomberBT, FormAyakBilekBT

llm = get_llm()

def node_router(state: GraphState) -> dict:
    ''' Textin hangi form tipine uygun olduğuna karar verir. '''
    print(f"\n--- DÜĞÜM (Hasta: {state['patient_name']}): Router ---")
    
    text_chunk = state.get("text_chunk", "")

    print("DEBUG (Router): Analiz edilecek metin bloğu:")
    print("-------------------------------------------")
    print(text_chunk)
    print("-------------------------------------------")

    if text_chunk.startswith("HATA:") or text_chunk.startswith("ERROR:"):
        return {"form_type": "undefined", "error": text_chunk}
    
    prompt = f"""
    Sen, tıbbi raporları sınıflandırma konusunda uzman bir asistansın.
    Görevin, sana verilen metin bloğunun konusunu analiz edip, aşağıdaki kategorilerden hangisine ait olduğunu belirlemektir.

    Şu adımları izle:
    1. Kategoriye karar verdiğinde formundaki findings kısmının tamamı sana verilen metinde geçmese de eklemelisin çünkü bazı doktorlar normal olan kısımları okumuyorlar, sadece değiştirilmiş yerlerini varsayılan cümlelerin yerine koyarak ver.


    KATEGORİLER:
    - 'ust_batin': Eğer metin ağırlıklı olarak üst batın BT bulguları, raporları veya ilgili terimler içeriyorsa.
    - 'alt_batin': Eğer metin ağırlıklı olarak alt batın BT bulguları, raporları veya ilgili terimler içeriyorsa.
    - 'toraks': Eğer metin ağırlıklı olarak kontrastsız toraks BT bulguları, raporları veya ilgili terimler içeriyorsa.
    - 'kontrast_toraks': Eğer metin ağırlıklı olarak kontrastlı toraks BT bulguları, raporları veya ilgili terimler içeriyorsa.
    - 'ayak_bilek': Eğer metin ağırlıklı olarak ayak bileği BT bulguları, raporları veya ilgili terimler içeriyorsa.
    - 'beyin': Eğer metin ağırlıklı olarak beyin BT bulguları, raporları veya ilgili terimler içeriyorsa.
    - 'lomber': Eğer metin ağırlıklı olarak lomber BT bulguları, raporları veya ilgili terimler içeriyorsa.
    - 'undefined': Eğer metin bu kategorilerden birine girmiyorsa veya tıbbi bir içerik değilse.

    
    METİN:
    ---
    {text_chunk}
    ---
    """
    
    try:
        routing_chain = get_routing_chain(llm)
        result = routing_chain.invoke(prompt)
        form_type = result.form_type
        print(f"Router kararı: {form_type}")
        return {"form_type": form_type}
    except Exception as e:
        print(f"HATA (Router): LLM çağrısı sırasında hata oluştu: {e}")
        return {"form_type": "undefined", "error": f"Router LLM hatası: {e}"}


def node_extract_ust_batin(state: GraphState) -> dict:
    """Ust Batın formuna göre veri çıkarır."""
    print(f"--- DÜĞÜM (Hasta: {state['patient_name']}): Extract Ust Batın ---")
    extraction_chain = get_extraction_chain(llm, FormUstBatinBT)
    default_text = FormUstBatinBT.model_fields['findings'].default
    
    prompt = f"""
    Aşağıdaki varsayılan 'findings' metnini baz al.
    Ardından, verilen transkript metnindeki bilgilere göre bu varsayılan metni güncelle.
    Eğer transkriptte normal dışı bir bulgu varsa, ilgili cümleyi değiştir.
    Eğer transkriptte bir bilgi yoksa, varsayılan normal cümleyi koru.
    
    Varsayılan Metin:
    {default_text}
    
    Transkript:
    {state["text_chunk"]}
    
    Sadece güncellenmiş 'findings' metnini döndür.
    """
    result = extraction_chain.invoke(prompt)
    return {"extracted_data": result.dict()}

def node_extract_alt_batin(state: GraphState) -> dict:
    """Alt Batın formuna göre veri çıkarır."""
    print(f"--- DÜĞÜM (Hasta: {state['patient_name']}): Extract Alt Batın ---")
    extraction_chain = get_extraction_chain(llm, FormAltBatinBT)
    default_text = FormAltBatinBT.model_fields['findings'].default
    
    prompt = f"""
    Aşağıdaki varsayılan 'findings' metnini baz al.
    Ardından, verilen transkript metnindeki bilgilere göre bu varsayılan metni güncelle.
    Eğer transkriptte normal dışı bir bulgu varsa, ilgili cümleyi değiştir.
    Eğer transkriptte bir bilgi yoksa, varsayılan normal cümleyi koru.
    
    Varsayılan Metin:
    {default_text}
    
    Transkript:
    {state["text_chunk"]}
    
    Sadece güncellenmiş 'findings' metnini döndür.
    """
    result = extraction_chain.invoke(prompt)
    return {"extracted_data": result.dict()}

def node_extract_toraks(state: GraphState) -> dict:
    """Toraks BT     formuna göre veri çıkarır."""
    print(f"--- DÜĞÜM (Hasta: {state['patient_name']}): Extract Toraks ---")
    extraction_chain = get_extraction_chain(llm, FormToraksBT)
    default_text = FormToraksBT.model_fields['findings'].default
    
    prompt = f"""
    Aşağıdaki varsayılan 'findings' metnini baz al.
    Ardından, verilen transkript metnindeki bilgilere göre bu varsayılan metni güncelle.
    Eğer transkriptte normal dışı bir bulgu varsa, ilgili cümleyi değiştir.
    Eğer transkriptte bir bilgi yoksa, varsayılan normal cümleyi koru.
    
    Varsayılan Metin:
    {default_text}
    
    Transkript:
    {state["text_chunk"]}
    
    Sadece güncellenmiş 'findings' metnini döndür.
    """
    result = extraction_chain.invoke(prompt)
    return {"extracted_data": result.dict()}

def node_extract_kontrast_toraks(state: GraphState) -> dict:
    """Kontrast Toraks BT formuna göre veri çıkarır."""
    print(f"--- DÜĞÜM (Hasta: {state['patient_name']}): Extract Kontrast Toraks ---")
    extraction_chain = get_extraction_chain(llm, FormKontrastToraksBT)
    default_text = FormKontrastToraksBT.model_fields['findings'].default
    
    prompt = f"""
    Aşağıdaki varsayılan 'findings' metnini baz al.
    Ardından, verilen transkript metnindeki bilgilere göre bu varsayılan metni güncelle.
    Eğer transkriptte normal dışı bir bulgu varsa, ilgili cümleyi değiştir.
    Eğer transkriptte bir bilgi yoksa, varsayılan normal cümleyi koru.
    
    Varsayılan Metin:
    {default_text}
    
    Transkript:
    {state["text_chunk"]}
    
    Sadece güncellenmiş 'findings' metnini döndür.
    """
    result = extraction_chain.invoke(prompt)
    return {"extracted_data": result.dict()}

def node_extract_beyinbt(state: GraphState) -> dict:
    """Beyin BT formuna göre veri çıkarır."""
    print(f"--- DÜĞÜM (Hasta: {state['patient_name']}): Extract Beyin BT ---")
    extraction_chain = get_extraction_chain(llm, FormBeyinBT)
    default_text = FormBeyinBT.model_fields['findings'].default
    
    prompt = f"""
    Aşağıdaki varsayılan 'findings' metnini baz al.
    Ardından, verilen transkript metnindeki bilgilere göre bu varsayılan metni güncelle.
    Eğer transkriptte normal dışı bir bulgu varsa, ilgili cümleyi değiştir.
    Eğer transkriptte bir bilgi yoksa, varsayılan normal cümleyi koru.
    
    Varsayılan Metin:
    {default_text}
    
    Transkript:
    {state["text_chunk"]}
    
    Sadece güncellenmiş 'findings' metnini döndür.
    """
    result = extraction_chain.invoke(prompt)
    return {"extracted_data": result.dict()}

def node_extract_lomber(state: GraphState) -> dict:
    """Lomber formuna göre veri çıkarır."""
    print(f"--- DÜĞÜM (Hasta: {state['patient_name']}): Extract Lomber ---")
    extraction_chain = get_extraction_chain(llm, FormLomberBT)
    default_text = FormLomberBT.model_fields['findings'].default
    
    prompt = f"""
    Aşağıdaki varsayılan 'findings' metnini baz al.
    Ardından, verilen transkript metnindeki bilgilere göre bu varsayılan metni güncelle.
    Eğer transkriptte normal dışı bir bulgu varsa, ilgili cümleyi değiştir.
    Eğer transkriptte bir bilgi yoksa, varsayılan normal cümleyi koru.
    
    Varsayılan Metin:
    {default_text}
    
    Transkript:
    {state["text_chunk"]}
    
    Sadece güncellenmiş 'findings' metnini döndür.
    """
    result = extraction_chain.invoke(prompt)
    return {"extracted_data": result.dict()}
 
def node_extract_ayak_bilek(state: GraphState) -> dict:
    """Ayak Bilek formuna göre veri çıkarır."""
    print(f"--- DÜĞÜM (Hasta: {state['patient_name']}): Extract Ayak Bilek ---")
    extraction_chain = get_extraction_chain(llm, FormAyakBilekBT)
    default_text = FormAyakBilekBT.model_fields['findings'].default
    
    prompt = f"""
    Aşağıdaki varsayılan 'findings' metnini baz al.
    Ardından, verilen transkript metnindeki bilgilere göre bu varsayılan metni güncelle.
    Eğer transkriptte normal dışı bir bulgu varsa, ilgili cümleyi değiştir.
    Eğer transkriptte bir bilgi yoksa, varsayılan normal cümleyi koru.
    
    Varsayılan Metin:
    {default_text}
    
    Transkript:
    {state["text_chunk"]}
    
    Sadece güncellenmiş 'findings' metnini döndür.
    """
    result = extraction_chain.invoke(prompt)
    return {"extracted_data": result.dict()}

def node_handle_error(state: GraphState) -> dict:
    """Belirsiz durumlarda hata durumu oluşturur."""
    print(f"--- DÜĞÜM (Hasta: {state['patient_name']}): Handle Error ---")
    err_msg = state.get("error", "Bu hastaya ait metin içeriği anlaşılamadı veya ilgili form bulunamadı.")
    return {"error": err_msg, "extracted_data": None}