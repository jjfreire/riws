from elasticsearch import Elasticsearch

#Conexión local Elasticsearch
es = Elasticsearch(hosts=["http://localhost:9200"])

doc1= {
    "title": "tecnico informatico (a)",
    "company": "ZAidAN it solutions",
    "description": "Para labores de cambio de equipos (apoyo) en el Aeropuerto de Pamplona, No\u00e1in, se requiere: \r\n\r\nTecnico/a Microinform\u00e1tico/a\r\n\r\n- Formaci\u00f3n en el \u00e1rea de inform\u00e1tica\r\n- Experiencia comprobable en servicio inform\u00e1ticos de por lo menos 1 a\u00f1o (incluye pr\u00e1cticas).\r\n- Disponibilidad la semana del 11 de noviembre (5-6 d\u00edas, trabajo puntual) con posibilidad de realizar otros proyectos luego.\r\n\r\n- Disponibilidad para realizar cursos de prevenci\u00f3n\r\n- Salario: 15.876\u20ac brutos al a\u00f1o",
    "link": "www.infojobs.net/noain-valle-de-elorz-noain-elortzibar/tecnico-informatico/of-i40719387a94e11a23f770f89883b14?applicationOrigin=search-new&page=1&sortBy=PUBLICATION_DATE",
    "salary": "15.000\u00a0\u20ac - 16.000\u00a0\u20ac Bruto/a\u00f1o",
    "duration": "Contrato fijo discontinuo",
    "workday": "Jornada completa",
    "location": "No\u00e1in (Valle de Elorz)/Noain (Elortzibar)",
    "modality": "Presencial"
}

#Insertar documento
es.index(index= "trabajos", id=1, body=doc1)