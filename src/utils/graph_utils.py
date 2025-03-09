from typing import List

from langgraph.graph import StateGraph


class BaseGraph(object):
    def __init__(self, state):
        self.state = state
        self.agents: List = []
        self.edges = []
        self.builder = StateGraph(self.state)

    def add_nodes(self, agent=None, name=""):
        if agent:
            self.builder.add_node(name or agent.__name__, agent)
        for _agent in self.agents:
            self.builder.add_node(_agent.__name__, _agent)

    def add_edges(self, source, target: str):
        return self.edges.append((source, target))

    def add_conditional_edges(self):
        NotImplementedError("Need to implement from sub-graph end")

    def build_graph(self, checkpointer=None, save_graph=False, graph_path=None):
        self.add_nodes()
        for edge in self.edges:
            self.builder.add_edge(edge[0], edge[1])
        app = self.builder.compile(checkpointer=checkpointer)
        if save_graph:
            graph_plot = app.get_graph().draw_mermaid_png()
            if not graph_path:
                graph_path = f"output.png"
            with open(graph_path, "wb") as f:
                f.write(graph_plot)
        print("Graph built successfully..!")
        return app

    async def run(self, memory, input_payload, config=None):
        app = self.build_graph(checkpointer=memory, save_graph=True)
        return await app.ainvoke(input_payload, config=config)
