from pydantic import BaseModel,Field
from typing import Optional,List

class PatientInfos(BaseModel):
    name:str = Field(None,description="Name of the patient")
    surname:str = Field(None,description="Surname of the patient")

class FormUstBatinBT(BaseModel):
    PatientInfos:str=Field(description="Informations of the relevant patient")
    findings:str=("Karaciğer normal konum ve boyuttadır. Karaciğer parankim dansitesi tabiidir. Safra kesesi normal lokalizasyonda ve büyüklükte izlenmiştir. İntra ve ekstrahepatik safra yollarına ait belirgin bir patoloji saptanmadı. Pankreas normal büyüklükte, dansitesi homojendir. Dalak normal konum ve boyuttadır. Parankim dansitesi tabiidir. Bilateral sürrenal glandlara ait belirgin bir patoloji dikkati çekmemiştir. Her iki böbrek normal lokalizasyon ve boyuttadır. Parankim kalınlıkları tabiidir. Bilateral böbrek toplayıcı sisteminde dilatasyon yada taş saptanmadı. İntraabdominal loküle veya serbest sıvı koleksiyonu, serbest hava saptanmadı. İnceleme alanına giren kemik yapılarda belirgin acil gross patoloji saptanmadı.")

class FormAltBatinBT(BaseModel):
    PatientInfos:str=Field(description="Informations of the relevant patient")
    findings:str=("İnceleme sınırlarında kesit alanına giren intestinal anslar ve kolon duvar kalınlıkları normaldir. Mesane konturları düzgün, dolumu homojendir. Internal genital organlar yaş ile uyumlu görünümdedir. İntrapelvik loküle veya serbest sıvı koleksiyonu, serbest hava saptanmadı. İncelemeye dahil kemik yapılarda fraktür saptanmadı.")

class FormToraksBT(BaseModel):
    PatientInfos:str=Field(description="Informations of the relevant patient")
    findings:str=("Trakea, karina ve her iki ana bronş açıktır.Mediastende ya da hiluslarda kitle-LAP saptanmamıştır. Kalp boyutu normaldir.Plevral ya da perikardial effüzyon izlenmemiştir.Akciğer parankim alanlarının değerlendirilmesinde, aktif infiltrasyon ya da spiküler konturlu kitle lezyonu izlenmemiştir.Kesitlere dahil kemik yapıların görünümü tabiidir.")

class FormKontrastToraksBT(BaseModel):
    PatientInfos:str=Field(description="Informations of the relevant patient")
    findings:str=("İnceleme IV. kontrast madde uygulanarak gerçekleştirilmiştir.Toraks simetriktir.Kalp normal boyutlardadır. Perikardial ve plevral effüzyon izlenmedi.Mediastinal-hiler patolojik boyutta lenf nodu izlenmedi.Her iki akciğer parankiminde belirgin infiltratif ve mass lezyon saptanmadı.İnceleme alanına giren kemik yapılarda fraktür izlenmedi.")

class FormLomberBT(BaseModel):
    PatientInfos:str=Field(description="Informations of the relevant patient")
    findings:str=("Lomber  lordoz tabiidir.Lomber vertebra korpus yükseklikleri doğaldır. Vertebra korpuslarında belirgin fraktür bulgusu izlenmedi. Spinal kanal çapı doğaldır. Paravertebral yumuşak doku planları olağandır.")

class FormBeyinBT(BaseModel):
    PatientInfos:str=Field(description="Informations of the relevant patient")
    findings:str=("IV. ventrikül orta hatta ve normal genişliktedir. Serebellum, pons ve mezensefalon dansiteleri BT çözünürlüğü dahilinde doğaldır. Bazal ganglionlar ve talamuslar normaldir. Serebral parankim normal olarak değerlendirilmiştir. Serebral sulkus derinlikleri ve ventriküler sistem genişliği yaş ile uyumludur. Orta hat yapılarda shift izlenmemiştir. Akut parankimal patoloji izlenmedi. Kranial kemik yapılarda fraktür saptanmadı. İntrakranial kanama bulgusu saptanmamıştır.")

class FormAyakBilekBT(BaseModel):
    PatientInfos:str=Field(description="Informations of the relevant patient")
    findings:str=("Ayak bileğini oluşturan kemik yapıların kortikal bütünlükleri tam olup, belirgin fraktür bulgusu saptanmamıştır. Yumuşak dokularda  belirgin patoloji saptanmadıİnceleme alanına giren kemik yapılarda fraktür izlenmedi.")


class PatientTextChunk(BaseModel):
    patient_name: str = Field(description="The full name or a clear identifier of the detected patient (e.g., 'Ahmet Yılmaz').")
    related_text: str = Field(description="The combined text of all sentences from the entire transcript that relate only to this patient.")

class TranscriptAnalysis(BaseModel):
    patient_chunks: List[PatientTextChunk]

    
"""Hastanıza yapılan Lomber BT incelemesinde;

Lomber  lordoz tabiidir.
**Lomber vertebralarda dejeneratif değişiklikler izlenmiştir.  
**L5-S1 eklem diski yüzüne bakan platolarda skleroz artışı izlenmiştir. Bu düzeyde intervertebral disk aralığında vakum fenomeni mevcuttur.   
Lomber vertebra korpus yükseklikleri doğaldır.
Vertebra korpuslarında belirgin fraktür bulgusu izlenmedi.
Spinal kanal çapı doğaldır.
Paravertebral yumuşak doku planları olağandır. --- lomber örneği



Tarih : 27/11/2025
ID : 2003012775 AcN: TRN8064349
Hasta Adı : BOZYAKALI MUNIRE
Bulgular :

Hastanıza yapılan Sağ Ayak Bileği BT incelemesinde;

**Sağda fibulada medüller yerleşimli milimetrik basit kistik lezyon izlenmiştir.  
Ayak bileğini oluşturan kemik yapıların kortikal bütünlükleri tam olup, belirgin fraktür bulgusu
saptanmamıştır.
**Kemik dokuda hafif dejeneratif değişiklikler izlenmiştir.   
Yumuşak dokularda  belirgin patoloji saptanmadı. --- ayak bilek örneği

""" 