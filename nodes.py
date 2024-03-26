import openai
import networkx as nx
import matplotlib.pyplot as plt
import json

# Function to parse the OpenAI response and create the knowledge graph
def create_graph_from_response(response):
    # Initialize an empty directed graph
    G = nx.DiGraph()

    # Process the response line by line
    for line in response.split('\n'):
        # Look for lines that represent graph edges in the expected format
        if "->" in line:
            # Split the line into source and target
            parts = line.split("->")
            source = parts[0].strip()
            target = parts[1].strip().rstrip(";")
            # Add an edge to the graph
            G.add_edge(source, target)

    return G

def generate_knowledge_graph(cpp_code):
    openai.api_key = 'api-key'  # Use your actual API key here

    # Craft a prompt that guides the model to list entities and describe relationships
    prompt = (
        "Please analyze the following C++ code and generate a knowledge graph.\n\n"
        "Code:\n" + cpp_code + "\n\n"
        "List the relationships in the code as edges in the following format:\n"
        "ClassA -> ClassB;\nFunctionX -> VariableY;\n"
    )

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Make sure to use the appropriate model for the task
        messages=[
            {"role": "system", "content": "You are an assistant who can analyze C++ code."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extracting the structured response from the completion
    structured_response = response.choices[0].message['content']

    # Generate the knowledge graph from the response
    graph = create_graph_from_response(structured_response)
    return graph

# Replace with the path to your C++ code file
cpp_code_path = 'C:/Users/lalan/OneDrive/Desktop/demo.cpp'
with open(cpp_code_path, 'r') as file:
    cpp_code = file.read()

# Generate the knowledge graph
graph = generate_knowledge_graph(cpp_code)

# Draw the knowledge graph
pos = nx.spring_layout(graph)
nx.draw(graph, pos, with_labels=True, node_color="skyblue", node_size=2000, font_size=10)
plt.show()
print("done")
# data = {
#     "nodes": [{"id": n, **graph.nodes[n]} for n in graph.nodes],
#     "links": [{"source": u, "target": v} for u, v in graph.edges]
# }

# # Write to a JSON file
# with open("graph.json", "w") as f:
#     json.dump(data, f, indent=4)
# print("exported graph to json")
def graph_to_json(graph):
    # Convert the NetworkX graph to a JSON-friendly format
    nodes = [{"id": n, "group": graph.nodes[n].get('group', 1)} for n in graph.nodes]
    links = [{"source": u, "target": v} for u, v in graph.edges]
    return {"nodes": nodes, "links": links}

def save_graph_to_json(graph, filename="knowledge_graph.json"):
    # Convert the graph to JSON format
    graph_json = graph_to_json(graph)
    # Save the JSON data to a file
    try:
        with open("knowledge_graph.json", "w") as f:
            json.dump(graph_json, f, indent=4)
    except Exception as e:
        print(f"An error occurred: {e}")


# Replace the plotting part of your script with a call to save_graph_to_json
# after you've updated the global_graph
save_graph_to_json(graph, "knowledge_graph.json")
