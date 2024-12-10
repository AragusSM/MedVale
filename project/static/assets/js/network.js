// Function to show the section
function showSection(sectionId) {
    const sections = document.querySelectorAll('main .section');
    
    // Hide all sections
    sections.forEach(section => {
      section.classList.remove('active'); // Remove active class
      section.style.display = 'none'; // Hide the section
      section.style.opacity = '0'; // Reset opacity to 0
    });

    // Show the selected section with fade-in
    const selectedSection = document.getElementById(sectionId);
    selectedSection.style.display = 'block'; // Make it visible first
    requestAnimationFrame(() => {
      selectedSection.style.opacity = '1'; // Trigger fade-in
      selectedSection.classList.add('active'); // Add active class
    });

    // Initialize network only when the network section is shown
    if (sectionId === 'network') {
      initializeNetwork(); // Call the function to initialize the network
    }

    if (sectionId === 'journey'){
      initializeJourneyNetwork();
    }
}

  // Get references to popup elements
  const nodePopup = document.getElementById('nodePopup');
  const closePopupButton = document.getElementById('close-popup');

  // Function to open the node details popup
  function openNodePopup(nodeData) {
    // Set popup content
    document.getElementById('node-name').textContent = nodeData.label;
    document.getElementById('node-definition').textContent = nodeData.definition;
    
    // Clear previous properties and add new ones
    const propertiesList = document.getElementById('node-properties');
    propertiesList.innerHTML = ''; // Clear previous list
    nodeData.properties.forEach(property => {
      const listItem = document.createElement('li');
      listItem.textContent = property;
      propertiesList.appendChild(listItem);
    });

    // Show picture if it exists
    const nodePicture = document.getElementById('node-picture');
    if (nodeData.picture) {
      nodePicture.src = nodeData.picture;
      nodePicture.style.display = 'block'; // Make picture visible
    } else {
      nodePicture.style.display = 'none'; // Hide picture if none exists
    }

    // Show the popup
    nodePopup.style.display = 'block';
  }

  // References to edge popup elements
  const edgePopup = document.getElementById("edgePopup");
  const closeEdgePopupButton = document.getElementById("close-edge-popup");

  // Function to open the edge details popup
  function openEdgePopup(edgeData, fromNode, toNode) {
    const edgePopup = document.getElementById("edgePopup");

    // Set popup content
    document.getElementById("edge-label").textContent = edgeData.label || "No Label";
    document.getElementById("edge-description").textContent = edgeData.description || "";
    document.getElementById("edge-connection").textContent = `${fromNode.label} <-> ${toNode.label}`;

    // Show the popup
    edgePopup.style.display = "block";
  }

  // Function to close the edge popup
  closeEdgePopupButton.addEventListener("click", function () {
    edgePopup.style.display = "none";
  });


  // Function to close the popup
  closePopupButton.addEventListener('click', function() {
    nodePopup.style.display = 'none'; // Hide the popup when the close button is clicked
  });


  // Close popup when clicking outside the node popup
  window.addEventListener('click', function(event) {
    if (event.target === nodePopup) {
      nodePopup.style.display = 'none'; // Close if clicked outside
    }
  });


  function openJourneyNodePopup(nodeData) {
    const nodePopup = document.getElementById("nodePopup2");
    const nodeName = document.getElementById("node-name2");
    const nodeDefinition = document.getElementById("node-definition2");
    const nodeProperties = document.getElementById("node-properties2");
    const nodePictureContainer = document.getElementById("node-picture-container2");
    const nodePicture = document.getElementById("node-picture2");
  
    // Set node details
    nodeName.textContent = nodeData.label || `Node ${nodeData.id}`;
    nodeDefinition.textContent = nodeData.definition || "No definition available.";
    
    // Populate properties
    nodeProperties.innerHTML = "";
    if (nodeData.properties) {
      nodeData.properties.forEach(prop => {
        const li = document.createElement("li");
        li.textContent = prop;
        nodeProperties.appendChild(li);
      });
    } else {
      nodeProperties.innerHTML = "<li>No properties available.</li>";
    }
  
    // Set node picture (if available)
    if (nodeData.picture) {
      nodePicture.src = nodeData.picture;
      nodePicture.style.display = "block";
    } else {
      nodePicture.style.display = "none";
    }
  
    // Show the popup
    nodePopup.style.display = "block";
  
    // Close button functionality
    document.getElementById("close-popup2").onclick = () => {
      nodePopup.style.display = "none";
    };
  }

  function openJourneyEdgePopup(edgeData, fromNode, toNode) {
    const edgePopup = document.getElementById("edgePopup2");
    const edgeLabel = document.getElementById("edge-label2");
    const edgeDescription = document.getElementById("edge-description2");
    const edgeConnection = document.getElementById("edge-connection2");
  
    // Set edge details
    edgeLabel.textContent = edgeData.label || `Edge ${edgeData.id}`;
    edgeDescription.textContent = edgeData.description || "No description available.";
    edgeConnection.textContent = `Connects: ${fromNode.label || fromNode.id} ↔ ${toNode.label || toNode.id}`;
  
    // Show the popup
    edgePopup.style.display = "block";
  
    // Close button functionality
    document.getElementById("close-edge-popup2").onclick = () => {
      edgePopup.style.display = "none";
    };
  }
  
  

  function showLoader() {
    const loader = document.getElementById("network-loader");
    if (loader){
        loader.style.display = "block";
        console.log("Showing loader");
    }else{
        console.log("loader not found");
    }
    
  }
  
  function hideLoader() {
    const loader = document.getElementById("network-loader");
    if (loader){
        loader.style.display = "none";
        console.log("Hiding loader");
    }else{
        console.log("loader not found");
    }
  }

  function showLoader2() {
    const loader = document.getElementById("network-loader2");
    if (loader){
        loader.style.display = "block";
        console.log("Showing loader");
    }else{
        console.log("loader not found");
    }
    
  }
  
  function hideLoader2() {
    const loader = document.getElementById("network-loader2");
    if (loader){
        loader.style.display = "none";
        console.log("Hiding loader");
    }else{
        console.log("loader not found");
    }
  }

    // Parse JSON data from script tags
    const nodes = new vis.DataSet(JSON.parse(document.getElementById('nodes-data').textContent));
    const edges = new vis.DataSet(JSON.parse(document.getElementById('edges-data').textContent));

    // Parse the node lists from the script tag
    const nodeLists = JSON.parse(document.getElementById("nodelists-data").textContent);
    
    // Function to adjust the brightness of a color (to make it lighter for the node)
    function lightenColor(color, factor = 1.5) {
        // Convert color to RGB
        let r = parseInt(color.substring(1, 3), 16);
        let g = parseInt(color.substring(3, 5), 16);
        let b = parseInt(color.substring(5, 7), 16);
    
        // Lighten the color by increasing the RGB values (up to 255)
        r = Math.min(255, Math.floor(r * factor));
        g = Math.min(255, Math.floor(g * factor));
        b = Math.min(255, Math.floor(b * factor));
    
        // Convert back to hex
        return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
    }
    
    // Function to adjust the brightness of a color (to make it darker for the border)
    function darkenColor(color, factor = 0.5) {
        // Convert color to RGB
        let r = parseInt(color.substring(1, 3), 16);
        let g = parseInt(color.substring(3, 5), 16);
        let b = parseInt(color.substring(5, 7), 16);
    
        // Darken the color by reducing the RGB values
        r = Math.floor(r * factor);
        g = Math.floor(g * factor);
        b = Math.floor(b * factor);
    
        // Convert back to hex
        return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
    }

    // Function to update the node colors based on the active filters
    function updateNodeColors(network, nodes, nodeLists) {
        const colorMapping = {
            'gram_positive': '#1E3A8A', // Dark blue
            'gram_negative': '#DC2626', // Red
            'antimicrobials': '#10B981', // Green
            'fungi': '#F97316', // Orange
            'dna_viruses': '#5F3D91', // Purple
            'rna_viruses': '#F59E0B', // Yellow
            'parasites': '#6B4F3B', // Brown
            'gram_ind': '#EC4899' // Pink
        };

        // Log the lightened colors
        /*for (let key in colorMapping) {
            if (colorMapping.hasOwnProperty(key)) {
                console.log(`${key}: ${lightenColor(colorMapping[key])}`);
            }
        }*/

        
        const defaultColor = '#93C5FD'; // Light Blue
        // Prepare an array to store updated nodes with new color and border

        /*const lightenedDefaultColor = lightenColor(defaultColor); // Lightened default color for the nodes

        // Log the lightened default color to the console
        console.log(`Lightened Default Color: ${lightenedDefaultColor}`);*/
        const updatedNodes = nodes.get().map(node => {
            let nodeColor = defaultColor; // Default to light blue
            let borderColor = darkenColor(nodeColor); // Default border is darker than the node color
            
            if (nodeLists.gram_positive.some(n => n === node.id)) {
              nodeColor = colorMapping['gram_positive'];
            } else if (nodeLists.gram_negative.some(n => n === node.id)) {
              nodeColor = colorMapping['gram_negative'];
            } else if (nodeLists.gram_ind.some(n => n === node.id)) {
              nodeColor = colorMapping['gram_ind'];
            }else if (nodeLists.antimicrobials.some(n => n === node.id)) {
              nodeColor = colorMapping['antimicrobials'];
            } else if (nodeLists.fungi.some(n => n === node.id)) {
              nodeColor = colorMapping['fungi'];
            } else if (nodeLists.dna_viruses.some(n => n === node.id)) {
              nodeColor = colorMapping['dna_viruses'];
            } else if (nodeLists.rna_viruses.some(n => n === node.id)) {
              nodeColor = colorMapping['rna_viruses'];
            } else if (nodeLists.parasites.some(n => n === node.id)) {
              nodeColor = colorMapping['parasites'];
            }

            // Lighten the color for the node and darken the color for the border
            const lightNodeColor = lightenColor(nodeColor);
            borderColor = darkenColor(lightNodeColor);
        
            // Return the updated node with the new color and border color
            return {
                id: node.id,  // Ensure you use node.id as the unique identifier
                color: {
                    background: lightNodeColor,
                    border: borderColor
                }
            };
          });
        
          // Update the nodes in the DataSet
          nodes.update(updatedNodes);
        
          // Redraw the network to apply the color changes
          network.redraw();
    }

  // Initialize Network Function
  function initializeNetwork() {
    // Check if the network is already initialized
    if (window.networkInitialized) return;

    showLoader();

    // Initialize the network
    const container = document.getElementById("network_graph");
    const data = { nodes: nodes, edges: edges };
    const options = {
      nodes: {
        shape: "dot", // Use circle shape
        size: 20, // Set a consistent size for all nodes (you can adjust this size)
        font: {
          size: 14, // Set font size inside the node
          face: 'Arial', // Set font family
          bold: "bold",
          align: 'center', // Horizontally center the text
          vadjust: 0, // Vertical adjustment (no vertical shift)
        },
      },
      edges: {
        color: {
            color: '#97C2FC',
            highlight: '#00008B'
        },
        font: {
          size: 7.5, // Smaller font size for edges
          align: "middle"
        },
      },
      interaction: {
        hover: false,
        tooltipDelay: 0, // Disable tooltip
        navigationButtons: false, // Remove navigation buttons
      },
      physics: {
        enabled: true,
        stabilization: {
            iterations: 200, // Reduce iterations for faster stabilization
            updateInterval: 20,
            fit: true, // Keep the current fit behavior
            onlyDynamicEdges: false // Apply to all edges
        },
        barnesHut: {
            gravitationalConstant: -4000, // Increase gravitational pull for better clustering
            centralGravity: 0.1, // Increase to bring nodes closer to the center faster
            springLength: 200, // Shorten spring length for tighter layouts
            springConstant: 0.04 // Slightly increase for quicker stabilization
        }
      }
        
    };
    const network = new vis.Network(container, data, options);


    
    
    // Run the update after the network is initialized
    updateNodeColors(network, nodes, nodeLists);  // Apply color based on node class


    // Event: Hide loader when stabilization is done
    network.once("stabilizationIterationsDone", () => hideLoader());

    // Handle click on node
    network.on("click", function (params) {
      if (params.nodes.length > 0) {
        const nodeId = params.nodes[0];
        const nodeData = nodes.get(nodeId);
        openNodePopup(nodeData);
      }
    });

    // Handle edge selection
    network.on("selectEdge", function (params) {
      if (params.edges.length > 0) {
        const edgeId = params.edges[0];
        const edgeData = edges.get(edgeId);

        // Fetch the connected nodes
        const fromNode = nodes.get(edgeData.from);
        const toNode = nodes.get(edgeData.to);

        // Update the popup content
        openEdgePopup(edgeData, fromNode, toNode);
      }
    });

    // Store active filters
    let activeFilters = {
      nodes: [], // Filtered nodes
      class: [], // Selected classes
      edgeLabels: [], // Selected edge labels
    };

    // Populate the class filter dropdown with unique classes in case-insensitive alphabetical order
    function populateClassFilterDropdown() {
      const classFilterDropdown = document.getElementById("classFilterDropdown");

      // Clear previous options
      classFilterDropdown.innerHTML = '<option value="">Select Class</option>';

      // Collect all unique classes
      const allClasses = new Set();
      nodes.forEach(node => node.hierarchy.forEach(cls => allClasses.add(cls)));

      // Convert the set to an array, sort it alphabetically (case-insensitive), and populate the dropdown
      Array.from(allClasses)
        .sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' }))
        .forEach(cls => {
          const option = document.createElement("option");
          option.value = cls;
          option.textContent = cls;
          classFilterDropdown.appendChild(option);
        });
    }


    // Filter functionality
    document.getElementById("applyFilter").addEventListener("click", () => {

      showLoader();

      // Clear other filters
      activeFilters = { class: [], edgeLabels: [], nodes: [] };

      const selectedClasses = Array.from(classFilterDropdown.selectedOptions).map(opt => opt.value);

      // Update active filters with selected classes
      activeFilters.class = selectedClasses;

      if (selectedClasses.length === 0) {
        network.setData({ nodes, edges });
        return;
      }

      // Filter nodes that have at least one matching class in their hierarchy
      const filteredNodes = nodes.get().filter(node => {
        return node.hierarchy.some(cls => selectedClasses.includes(cls));
      });

      // Filter edges to only include those connected to the filtered nodes
      const filteredNodeIds = filteredNodes.map(node => node.id);
      const filteredEdges = edges.get().filter(edge => {
        return filteredNodeIds.includes(edge.from) && filteredNodeIds.includes(edge.to);
      });


      // Update the network with the filtered data
      network.setData({
        nodes: new vis.DataSet(filteredNodes),
        edges: new vis.DataSet(filteredEdges),
      });

      const order0 = document.getElementById("order0");
      order0.checked = true;

      // Event: Hide loader when stabilization is done
      network.once("stabilizationIterationsDone", () => hideLoader());

    });

    // Populate the edge label filter dropdown with unique edge labels in case-insensitive alphabetical order
    function populateEdgeLabelFilterDropdown() {
      const edgeLabelFilter = document.getElementById("edgeLabelFilter");

      // Clear previous options
      edgeLabelFilter.innerHTML = '<option value="">Select Edge</option>';

      // Collect all unique edge labels
      const allLabels = new Set();
      edges.forEach(edge => {
        if (edge.label) {
          allLabels.add(edge.label);
        }
      });

      // Convert the set to an array, sort it alphabetically (case-insensitive), and populate the dropdown
      Array.from(allLabels)
        .sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' }))
        .forEach(label => {
          const option = document.createElement("option");
          option.value = label;
          option.textContent = label;
          edgeLabelFilter.appendChild(option);
        });
    }



    // Apply the filter when the user selects a label
    document.getElementById("applyEdgeLabelFilter").addEventListener("click", () => {
      
      showLoader();
      // Clear other filters
      activeFilters = { class: [], edgeLabels: [], nodes: [] };

      // Get the selected edge label
      const selectedLabel = document.getElementById("edgeLabelFilter").value;

      // Update active filters with selected edge label
      activeFilters.edgeLabels = selectedLabel ? [selectedLabel] : [];


      if (!selectedLabel) {
        alert("Please select an edge label to filter!");
        filterLoader.style.display = "none"; // Hide the spinner if no label is selected
        return;
      }

      // Filter edges based on the selected label
      const filteredEdges = edges.get().filter(edge => {
        return edge.label === selectedLabel;
      });

      // Filter nodes that are connected by the filtered edges
      const filteredNodeIds = new Set();
      filteredEdges.forEach(edge => {
        filteredNodeIds.add(edge.from);
        filteredNodeIds.add(edge.to);
      });

      // Filter nodes that are part of the filtered edges
      const filteredNodes = nodes.get().filter(node => {
        return filteredNodeIds.has(node.id);
      });

      activeFilters.nodes = Array.from(filteredNodeIds);


      // Update the network with the filtered nodes and edges
      network.setData({
        nodes: new vis.DataSet(filteredNodes),
        edges: new vis.DataSet(filteredEdges),
      });

      const order1 = document.getElementById("order1");
      order1.checked = true;

      // Event: Hide loader when stabilization is done
      network.once("stabilizationIterationsDone", () => hideLoader());


    });

   // Populate the node filter dropdown with available node names (or IDs) in alphabetical order
    function populateNodeFilterDropdown() {
      const nodeFilterDropdown = document.getElementById("nodeFilterDropdown");

      // Clear previous options
      nodeFilterDropdown.innerHTML = '<option value="">Select Node</option>';

      // Collect nodes into an array
      const nodeArray = nodes.get().map(node => ({
        id: node.id,
        label: node.label || node.name || node.id, // Use label, name, or ID for display
      }));

      // Sort nodes alphabetically by their labels
      nodeArray.sort((a, b) => a.label.localeCompare(b.label, undefined, { sensitivity: 'base' }));


      // Populate the dropdown with sorted nodes
      nodeArray.forEach(node => {
        const option = document.createElement("option");
        option.value = node.id; // Use node ID for filtering
        option.textContent = node.label; // Display node label
        nodeFilterDropdown.appendChild(option);
      });
    }

    // Apply Node Filter
    document.getElementById("applyNodeFilter").addEventListener("click", () => {

      showLoader();

      // Clear other filters
      activeFilters = { class: [], edgeLabels: [], nodes: [] };

      // Get selected node
      const selectedNodeId = document.getElementById("nodeFilterDropdown").value;

      // Update active filters with selected node ID
      activeFilters.nodes = selectedNodeId ? [selectedNodeId] : [];

      if (!selectedNodeId) {
        alert("Please select a node to filter!");
        filterLoader.style.display = "none"; // Hide the spinner if no node is selected
        return;
      }

      // Filter nodes by selected node ID
      const filteredNodes = nodes.get().filter(node => {
        return node.id === selectedNodeId;
      });

      // Filter edges connected to the filtered node
      const filteredNodeIds = new Set(filteredNodes.map(node => node.id));
      const filteredEdges = edges.get().filter(edge => {
        return filteredNodeIds.has(edge.from) || filteredNodeIds.has(edge.to);
      });


      // Update network data
      network.setData({
        nodes: new vis.DataSet(filteredNodes),
        edges: new vis.DataSet(filteredEdges),
      });

      const order0 = document.getElementById("order0");
      order0.checked = true;

      // Event: Hide loader when stabilization is done
      network.once("stabilizationIterationsDone", () => hideLoader());


    });

    // Call this function when the page loads to populate the node filter dropdown
    populateNodeFilterDropdown();
    populateClassFilterDropdown();
    populateEdgeLabelFilterDropdown();


    function getNodesAndEdgesByOrder(filteredNodes, edges, order) {
      const nodeSet = new Set(filteredNodes.map(node => node.id));
      const edgeSet = new Set();

      let currentNodes = filteredNodes;

      for (let i = 0; i < order; i++) {
        const newEdges = [];
        const newNodes = [];

        // Add edges and connected nodes
        edges.forEach(edge => {
          const edgeFrom = edge.from || edge['from'];
          const edgeTo = edge.to || edge['to'];

          if (nodeSet.has(edgeFrom) || nodeSet.has(edgeTo)) {
            const edgeId = edge.id || `${edgeFrom}-${edgeTo}`;
            if (!edgeSet.has(edgeId)) {
              edgeSet.add(edgeId);
              newEdges.push(edge);

              // Add new connected nodes
              if (!nodeSet.has(edgeFrom)) newNodes.push(edgeFrom);
              if (!nodeSet.has(edgeTo)) newNodes.push(edgeTo);
            }
          }
        });

        // Add new nodes to the set
        newNodes.forEach(nodeId => nodeSet.add(nodeId));

        // Update current nodes for the next iteration
        currentNodes = newNodes.map(nodeId => nodes.get(nodeId));
      }

      // Convert edgeSet to an array of edges (handle array vs. vis.DataSet differences)
      const finalEdges = Array.from(edgeSet).map(edgeId => {
        if (edges instanceof vis.DataSet) {
          return edges.get(edgeId); // Use get() if it's a DataSet
        } else {
          // Use find() for plain arrays
          return edges.find(edge => edge.id === edgeId || `${edge.from}-${edge.to}` === edgeId);
        }
      });

      // Convert nodeSet to an array of nodes
      const finalNodes = Array.from(nodeSet).map(nodeId => nodes.get(nodeId));

      return { finalNodes, finalEdges };
    }

    // Handle render order change based on active filters
    document.querySelectorAll('input[name="renderOrder"]').forEach(radio => {
      radio.addEventListener("change", () => {

        showLoader();

        const selectedOrder = radio.value;

        // Get the filtered nodes and edges based on active filters
        const { filteredNodes, filteredEdges } = getFilteredNodesAndEdges();

        if (selectedOrder === "full") {
          // Show the full network
          network.setData({
            nodes: nodes, // Full nodes dataset
            edges: edges, // Full edges dataset
          });
        } else {
          // Apply the render order logic
          const renderOrder = parseInt(selectedOrder, 10);
          const { finalNodes, finalEdges } = getNodesAndEdgesByOrder(filteredNodes, filteredEdges, renderOrder);

          
          // Update the network with the new data
          network.setData({
            nodes: new vis.DataSet(finalNodes),
            edges: new vis.DataSet(finalEdges),
          });
        }

        // Event: Hide loader when stabilization is done
        network.once("stabilizationIterationsDone", () => hideLoader());


      });
    });

    function getFilteredNodesAndEdges() {
      // Filter nodes based on active filters
      const filteredNodes = nodes.get().filter(node => {
        // Apply class filter
        if (activeFilters.class.length > 0 && !activeFilters.class.some(cls => node.hierarchy.includes(cls))) {
          return false;
        }

        // Apply node filter
        if (activeFilters.nodes.length > 0 && !activeFilters.nodes.includes(node.id)) {
          return false;
        }

        return true;
      });

      // Filter edges based on active edge label filter
      const filteredEdges = edges.get();
      return { filteredNodes, filteredEdges };
    }



    // Mark network as initialized
    window.networkInitialized = true;
}
  
document.getElementById("toggleViewBtn").addEventListener("click", () => {
  showSection("journey");
});

document.getElementById("toggleViewBtn2").addEventListener("click", ()=>{
  showSection("network");
});


let currentNodeId = null; // Track the current node in the journey
let journeyNetwork = null; // Store the vis.js network instance
let journeyNodes = null; // Track nodes in the journey network
let journeyEdges = null; // Track edges in the journey network

// Function to initialize the journey network
function initializeJourneyNetwork() {
  showLoader2();
  const allNodes = nodes.get();
  if (allNodes.length === 0) return;

  // Start with a random node
  currentNodeId = allNodes[Math.floor(Math.random() * allNodes.length)].id;

  // Initialize the vis.js DataSets
  journeyNodes = new vis.DataSet([nodes.get(currentNodeId)]);
  journeyEdges = new vis.DataSet();

  // Render the network
  const container = document.getElementById("journey_graph");
  const data = { nodes: journeyNodes, edges: journeyEdges };
  const options = {
    nodes: {
      shape: "dot",
      size: 20,
    },
    edges: {
      font: {
        size: 12,
        align: "middle",
      },
      color: {
        color: "#97C2FC",
        highlight: "#00008B",
      },
    },
    physics: {
      enabled: true, // Disable physics for small networks
    },
  };

  journeyNetwork = new vis.Network(container, data, options);

  journeyNetwork.once("stabilizationIterationsDone", () => hideLoader2());
  

  // Populate the connected nodes selector
  populateScrollableButtons(currentNodeId);

  // Add event listener for node clicks
  journeyNetwork.on("click", function (params) {
    if (params.nodes.length > 0) {
      const nodeId = params.nodes[0];
      const nodeData = journeyNodes.get(nodeId);
      openJourneyNodePopup(nodeData); // Show the Journey node popup
    }
  });

  // Add event listener for edge clicks
  journeyNetwork.on("selectEdge", function (params) {
    if (params.edges.length > 0) {
      const edgeId = params.edges[0];
      const edgeData = journeyEdges.get(edgeId);

      // Fetch the connected nodes
      const fromNode = journeyNodes.get(edgeData.from);
      const toNode = journeyNodes.get(edgeData.to);

      // Show the Journey edge popup
      openJourneyEdgePopup(edgeData, fromNode, toNode);
    }
  });
}

// Function to populate scrollable buttons for connected nodes
function populateScrollableButtons(nodeId) {
  const connectedEdges = edges.get().filter(edge => edge.from === nodeId || edge.to === nodeId);
  const connectedNodes = connectedEdges.map(edge =>
    nodes.get(edge.from === nodeId ? edge.to : edge.from)
  );

  const nodeButtonsContainer = document.getElementById("nodeButtons");
  nodeButtonsContainer.innerHTML = ""; // Clear previous buttons

  connectedNodes.forEach(node => {
    if (!journeyNodes.get(node.id)) {
      const button = document.createElement("button");
      button.textContent = node.label || `Node ${node.id}`;
      button.className = "btn btn-primary";
      button.style.marginBottom = "10px";

      button.onclick = () => {
        fetch(`/get_text?selected_node_id=${node.id}&previous_node_id=${nodeId}`) // Send both IDs
          .then(response => response.json())
          .then(data => {
            const text = data.text; // Get the text from the Flask response

            // Trigger the typewriter effect with the fetched text
            typeWriterEffect("typewriterParagraph", text, 10, 5); // Adjust speed and step
          })
          .catch(error => {
            console.error("Error fetching text:", error);
          });

        addNodeAndEdge(nodeId, node.id);
      };

      nodeButtonsContainer.appendChild(button);
    }
  });
}

// Function to add a new node and edge to the journey network
function addNodeAndEdge(fromNodeId, toNodeId) {
  // Add the new node
  const newNode = nodes.get(toNodeId);
  if (!journeyNodes.get(toNodeId)) {
    journeyNodes.add(newNode);
  }

  // Add the connecting edge
  const connectingEdge = edges.get().find(
    edge => (edge.from === fromNodeId && edge.to === toNodeId) || (edge.from === toNodeId && edge.to === fromNodeId)
  );
  if (!journeyEdges.get(connectingEdge.id)) {
    journeyEdges.add(connectingEdge);
  }

  // Update the current node and refresh the connected nodes
  currentNodeId = toNodeId;
  populateScrollableButtons(toNodeId);

  // Refresh the network with the updated DataSets
  journeyNetwork.setData({ nodes: journeyNodes, edges: journeyEdges });
}

let typingTimeouts = []; // Store timeouts for the typing animation

function clearTypingEffect() {
  // Clear all active timeouts
  typingTimeouts.forEach(timeout => clearTimeout(timeout));
  typingTimeouts = [];
}

function typeWriterEffect(elementId, text, speed, step = 1) {
  clearTypingEffect(); // Clear ongoing animations

  const element = document.getElementById(elementId);
  element.style.overflow = "hidden"; // Ensure no overflow by default
  element.style.whiteSpace = "pre-wrap"; // Preserve line breaks and wrapping
  element.style.wordWrap = "break-word"; // Break long words to fit

  let index = 0;

  function type() {
    if (index < text.length) {
      element.textContent += text.slice(index, index + step); // Add characters
      index += step; // Increment index

      // Scroll to the bottom of the container
      element.scrollTop = element.scrollHeight;

      const timeout = setTimeout(type, speed); // Schedule next animation step
      typingTimeouts.push(timeout); // Track timeout
    }
  }

  // Reset the content and start typing
  element.textContent = "";
  type();
}


let correctAnswer = ""; // Variable to store the correct answer

// Handle Generate Question Button Click
document.getElementById("generateQuestionBtn").addEventListener("click", () => {
  fetch("/generate_question")
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert("Error: " + data.error);
        return;
      }

      // Display the question
      const questionContainer = document.getElementById("questionContainer");
      const questionText = document.getElementById("questionText");
      const questionOptions = document.getElementById("questionOptions");
      const submitAnswerBtn = document.getElementById("submitAnswerBtn");

      questionContainer.style.display = "block";
      questionText.textContent = data.question;

      // Extract the correct answer
      correctAnswer = data.correct_option;

      // Render options as radio buttons
      questionOptions.innerHTML = ""; // Clear existing options
      data.options.forEach((option, index) => {
        const optionDiv = document.createElement("div");
        optionDiv.style.marginBottom = "10px";

        const radio = document.createElement("input");
        radio.type = "radio";
        radio.name = "mcqOption";
        radio.value = option;
        radio.id = `option${index}`;

        const label = document.createElement("label");
        label.htmlFor = `option${index}`;
        label.textContent = option;

        optionDiv.appendChild(radio);
        optionDiv.appendChild(label);
        questionOptions.appendChild(optionDiv);
      });

      // Show the Submit button
      submitAnswerBtn.style.display = "inline-block";
    })
    .catch(error => {
      console.error("Error generating question:", error);
    });
});

// Handle Submit Answer Button Click
document.getElementById("submitAnswerBtn").addEventListener("click", () => {
  const selectedOption = document.querySelector('input[name="mcqOption"]:checked');
  const feedbackElement = document.getElementById("answerFeedback");

  if (!selectedOption) {
    feedbackElement.textContent = "Please select an answer.";
    feedbackElement.style.color = "red";
    return;
  }

  if (selectedOption.value === correctAnswer) {
    feedbackElement.textContent = "Correct! Well done!";
    feedbackElement.style.color = "green";
  } else {
    feedbackElement.textContent = "Incorrect. Try again!";
    feedbackElement.style.color = "red";
  }
});





// Show the first section (home) by default on page load
document.addEventListener('DOMContentLoaded', () => {
    showSection('home');

    const paragraphText = "Select related concepts to build a pathway. A description of each new edge will be shown here";
    typeWriterEffect("typewriterParagraph", paragraphText, 20); // Adjust speed (in ms) as needed

});