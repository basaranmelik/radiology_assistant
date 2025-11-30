from langgraph.graph import StateGraph,END
from graph.state import GraphState
from graph.nodes import *
from schemas.form_schemas import FormUstBatinBT,FormAltBatinBT,FormToraksBT,FormKontrastToraksBT

def should_contiune(state:GraphState)->GraphState:
    ''' router nodedan sonra hangi yolu seçeceğine karar verir.'''
    if state["form_type"] =="ust_batin":
        return "extract_ust_batin"
    elif state["form_type"]=="alt_batin":
        return "extract_alt_batin"
    elif state["form_type"]=="toraks":
        return "extract_toraks"
    elif state["form_type"]=="kontrast_toraks":
        return "extract_kontrast_toraks"
    elif state["form_type"]=="ayak_bilek":
        return "extract_ayak_bilek"
    elif state["form_type"]=="beyin":
        return "extract_beyin"
    elif state["form_type"]=="lomber":
        return "extract_lomber"
    else:
        return "handle_error"
    
graph = StateGraph(GraphState)

graph.add_node("router",node_router)
graph.add_node("extract_ust_batin",node_extract_ust_batin)
graph.add_node("extract_alt_batin",node_extract_alt_batin)
graph.add_node("extract_toraks",node_extract_toraks)
graph.add_node("extract_kontrast_toraks",node_extract_kontrast_toraks)
graph.add_node("extract_ayak_bilek",node_extract_ayak_bilek)
graph.add_node("extract_beyinbt",node_extract_beyinbt)
graph.add_node("extract_lomber",node_extract_lomber)
graph.add_node("handle_error",node_handle_error)

graph.set_entry_point("router")

graph.add_conditional_edges(
    "router",
    should_contiune,
    {
        "extract_ust_batin":"extract_ust_batin",
        "extract_alt_batin":"extract_alt_batin",
        "extract_toraks":"extract_toraks",
        "extract_kontrast_toraks":"extract_kontrast_toraks",
        "extract_ayak_bilek":"extract_ayak_bilek",
        "extract_beyinbt":"extract_beyinbt",
        "extract_lomber":"extract_lomber",
        "handle_error":"handle_error",        
    }
)

graph.add_edge("extract_ust_batin",END)
graph.add_edge("extract_alt_batin",END)
graph.add_edge("extract_toraks",END)
graph.add_edge("extract_kontrast_toraks",END)
graph.add_edge("extract_ayak_bilek",END)
graph.add_edge("extract_beyinbt",END)
graph.add_edge("extract_lomber",END)
graph.add_edge("handle_error",END)

app = graph.compile()