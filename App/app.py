import gradio as gr
from document_loader import DocumentLoader, VectorStore
from rag_agent import RAGAgent
from code_optimizer import CodeOptimizer
from gpu_mentor import GPUMentor
from langchain.tools.retriever import create_retriever_tool
from benchmark import run_benchmark  # Using the updated benchmark implementation

class GPUMentorApp:
    """Main application class for the GPU Mentor."""
    
    def __init__(self):
        self.gpu_mentor = None
        self.initialize_system()
    
    def initialize_system(self):
        """Initialize all components of the GPU Mentor system."""
        print("🚀 Initializing GPU Mentor System...")
        
        try:
            # Load and process documents
            print("📚 Loading documents...")
            doc_loader = DocumentLoader()
            docs = doc_loader.load_documents()
            doc_splits = doc_loader.split_documents(docs)
            
            # Create vector store
            print("🔍 Creating vector store...")
            vector_store = VectorStore()
            retriever = vector_store.create_vectorstore(doc_splits)
            
            # Create retriever tool
            retriever_tool = create_retriever_tool(
                retriever,
                "retrieve_python_gpu_acceleration",
                "Search and return information about accelerating Python code using GPU with RAPIDS and CuPy."
            )
            
            # Initialize RAG agent
            print("🤖 Initializing RAG agent...")
            rag_agent = RAGAgent()
            rag_agent.set_retriever_tool(retriever_tool)
            
            # Initialize code optimizer
            print("⚡ Initializing code optimizer...")
            code_optimizer = CodeOptimizer(rag_agent)
            
            # Initialize GPU mentor
            print("🎓 Initializing GPU mentor...")
            self.gpu_mentor = GPUMentor(rag_agent, code_optimizer)
            
            print("✅ GPU Mentor System initialized successfully!")
            
        except Exception as e:
            print(f"❌ Error initializing system: {e}")
            self.gpu_mentor = None
    
    def create_interface(self):
        """Create the Gradio interface."""
        if not self.gpu_mentor:
            return gr.Interface(
                fn=lambda: "System not initialized properly. Please check the logs.",
                inputs=[],
                outputs=gr.Textbox(label="Error"),
                title="GPU Mentor - Initialization Error"
            )
        
        # Sample code examples
        sample_codes = {
            "Matrix Multiplication": """import numpy as np

# Create large matrices
size = 1000
A = np.random.rand(size, size).astype(np.float32)
B = np.random.rand(size, size).astype(np.float32)

# Matrix multiplication
C = np.matmul(A, B)

print(f"Result shape: {C.shape}")
print(f"Sum of result: {np.sum(C)}")""",
            
            "DataFrame Operations": """import pandas as pd
import numpy as np

# Create sample dataframe
n_rows = 100000
df = pd.DataFrame({
    'A': np.random.randn(n_rows),
    'B': np.random.randn(n_rows),
    'C': np.random.choice(['X', 'Y', 'Z'], n_rows),
    'D': np.random.randint(1, 100, n_rows)
})

# Perform operations
result = df.groupby('C').agg({
    'A': 'mean',
    'B': 'std',
    'D': 'sum'
})

print(result)""",
            
            "Machine Learning": """from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import numpy as np

# Generate sample data
X, _ = make_blobs(n_samples=10000, centers=10, 
                  n_features=20, random_state=42)

# Perform clustering
kmeans = KMeans(n_clusters=10, random_state=42)
labels = kmeans.fit_predict(X)

print(f"Cluster centers shape: {kmeans.cluster_centers_.shape}")
print(f"Labels shape: {labels.shape}")"""
        }
        
        # Create interface
        # Custom CSS for better layout
        custom_css = """
        .analysis-results {
            min-height: 300px;
            max-height: 500px;
            overflow-y: auto;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 16px;
        }
        .execution-results {
            min-height: 200px;
            max-height: 300px;
            overflow-y: auto;
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            padding: 12px;
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 12px;
        }
        .code-analysis-tab {
            height: 100vh;
        }
        .code-input-row {
            margin-bottom: 16px;
        }
        .execution-row {
            margin-bottom: 16px;
        }
        .button-bar {
            margin: 16px 0;
            gap: 8px;
        }
        .gradio-container {
            max-width: 100% !important;
        }
        /* Enhanced code editor styling */
        .code-input .cm-editor {
            border: 2px solid #3b82f6;
            border-radius: 8px;
        }
        .code-output .cm-editor {
            border: 2px solid #10b981;
            border-radius: 8px;
            background-color: #f8fafc;
        }
        /* Make code editors more prominent */
        .gr-code {
            font-family: 'Monaco', 'Consolas', 'Courier New', monospace;
        }
        """
        
        with gr.Blocks(
            title="GPU Mentor - AI-Powered GPU Acceleration Assistant", 
            theme=gr.themes.Soft(),
            css=custom_css
        ) as interface:
            gr.Markdown("""
            # 🚀 GPU Mentor - AI-Powered GPU Acceleration Assistant
            
            Learn how to accelerate your Python code using NVIDIA Rapids libraries (CuPy, cuDF, cuML).
            Get AI-powered code optimization suggestions and educational guidance.
            """)
            
            with gr.Tab("💬 Chat with GPU Mentor"):
                with gr.Row():
                    with gr.Column(scale=2):
                        chatbot = gr.Chatbot(
                            height=600, 
                            label="Conversation (with Memory)",
                            type="messages",
                            value=[{
                                "role": "assistant", 
                                "content": """👋 **Welcome to GPU Mentor!**

I'm your AI assistant for GPU acceleration with NVIDIA Rapids libraries. 

🧠 **New Feature**: I now have **conversation memory**! You can:
- Ask follow-up questions and I'll remember our previous discussion
- Reference earlier topics with phrases like "what about...", "tell me more...", etc.
- Build on our conversation naturally

🚀 **What I can help with**:
- Analyze Python code for GPU optimization opportunities  
- Convert NumPy → CuPy, Pandas → cuDF, scikit-learn → cuML
- Explain GPU acceleration concepts and best practices
- Answer follow-up questions based on our conversation

Feel free to ask questions about GPU acceleration or paste code for analysis!"""
                            }]
                        )
                        
                        with gr.Row():
                            message_input = gr.Textbox(
                                placeholder="Ask about GPU acceleration, or ask follow-up questions...",
                                label="Your Question",
                                scale=4
                            )
                            submit_btn = gr.Button("Send", variant="primary", scale=1)
                        
                        clear_btn = gr.Button("🧹 Clear Chat & Memory", variant="secondary")
                    
                    with gr.Column(scale=1):
                        sample_dropdown = gr.Dropdown(
                            choices=list(sample_codes.keys()),
                            label="Choose Sample",
                            interactive=True
                        )
                        load_sample_btn = gr.Button("Load Sample", variant="secondary")
                        
                        code_input = gr.Code(
                            value="",
                            label="Code to Analyze (Optional)",
                            language="python",
                            lines=20,
                            interactive=True
                        )
            
            with gr.Tab("🔍 Code Analysis & Optimization"):
                # Top row: Code input and GPU optimized code side by side
                with gr.Row(elem_classes=["code-input-row"]):
                    with gr.Column(scale=1):
                        analyze_code = gr.Code(
                            value="",
                            label="💻 Code to Analyze",
                            language="python",
                            lines=15,
                            interactive=True,
                            elem_classes=["code-input"]
                        )
                    
                    with gr.Column(scale=1):
                        optimized_code = gr.Code(
                            value="",
                            label="🚀 GPU-Optimized Code",
                            language="python",
                            lines=15,
                            interactive=False,
                            elem_classes=["code-output"]
                        )
                
                # Button bar: Sample dropdown, load, analyze, and clear buttons
                with gr.Row(elem_classes=["button-bar"]):
                    analysis_sample_dropdown = gr.Dropdown(
                        choices=list(sample_codes.keys()),
                        label=None,
                        interactive=True,
                        scale=2,
                        elem_classes=["sample-dropdown"]
                    )
                    load_analysis_sample_btn = gr.Button("📥 Load Sample", variant="secondary", scale=1)
                    analyze_btn = gr.Button("🔍 Analyze Code", variant="primary", scale=2)
                    benchmark_btn = gr.Button("⚡ Benchmark on Sol", variant="primary", scale=2)
                    clear_code_btn = gr.Button("🗑️ Clear", variant="secondary", scale=1)
                
                # No longer needed - using only the markdown outputs below
                
                # Execution results row: Show formatted execution outputs below code boxes
                with gr.Row(elem_classes=["execution-row"]):
                    with gr.Column(scale=1):
                        original_execution_output = gr.Markdown(
                            label="🖥️ Original Code Execution",
                            value="**Original Code Execution Results**\n\nClick '⚡ Benchmark on Sol' to execute the original code on the Sol supercomputer and see timing results.",
                            elem_classes=["execution-results"]
                        )
                    
                    with gr.Column(scale=1):
                        optimized_execution_output = gr.Markdown(
                            label="🚀 GPU Code Execution", 
                            value="**GPU-Optimized Code Execution Results**\n\nClick '⚡ Benchmark on Sol' to execute the GPU-optimized code and compare performance.",
                            elem_classes=["execution-results"]
                        )

                def benchmark_handler(cpu_code, gpu_code):
                    if not cpu_code.strip() or not gpu_code.strip():
                        return "No code provided for benchmarking.", "No code provided for benchmarking."
                    
                    try:
                        # Run the benchmark and get formatted markdown outputs
                        original_md, optimized_md = self.gpu_mentor.run_code_comparison(cpu_code, gpu_code)
                        return original_md, optimized_md
                    except Exception as e:
                        error_msg = f"Error running benchmark: {str(e)}"
                        return error_msg, error_msg

                # Enable Benchmark only if both code boxes are filled
                def enable_benchmark(cpu, gpu):
                    return bool(cpu.strip()) and bool(gpu.strip())
                analyze_code.change(enable_benchmark, [analyze_code, optimized_code], benchmark_btn)
                optimized_code.change(enable_benchmark, [analyze_code, optimized_code], benchmark_btn)

                benchmark_btn.click(
                    benchmark_handler,
                    inputs=[analyze_code, optimized_code],
                    outputs=[original_execution_output, optimized_execution_output]
                )
                
                # Bottom area: AI insights taking the rest of the space
                with gr.Row():
                    analysis_results = gr.Markdown(
                        label="🧠 AI Analysis & Recommendations",
                        value="**Welcome to GPU Code Analysis!**\n\nSelect code from the samples above or paste your own Python code, then click 'Analyze Code' to see:\n- AI-powered analysis of your code\n- GPU optimization opportunities\n- Performance improvement suggestions\n- Best practices recommendations",
                        elem_classes=["analysis-results"]
                    )
            
            with gr.Tab("📚 Learning Resources"):
                with gr.Row():
                    with gr.Column():
                        tutorial_topic = gr.Textbox(
                            placeholder="e.g., CuPy array operations, cuDF dataframes, cuML machine learning",
                            label="Tutorial Topic"
                        )
                        generate_tutorial_btn = gr.Button("Generate Tutorial", variant="primary")
                    
                    with gr.Column():
                        tutorial_content = gr.Markdown(label="Tutorial Content")
            
            with gr.Tab("📊 Execution Summary"):
                with gr.Row():
                    summary_btn = gr.Button("Get Execution Summary", variant="primary")
                    execution_summary = gr.Markdown(label="Execution Summary")
            
            # Event handlers
            def load_sample_code(sample_name):
                if sample_name and sample_name in sample_codes:
                    return sample_codes[sample_name]
                return ""
            
            def clear_chat():
                # Clear conversation memory in the RAG agent
                if self.gpu_mentor:
                    self.gpu_mentor.clear_conversation_memory()
                # Return a clean slate with a fresh welcome message
                return [{
                    "role": "assistant", 
                    "content": """👋 **Welcome back to GPU Mentor!**

🧹 **Chat memory cleared** - Starting fresh!

🧠 **Conversation Memory**: I can now remember our conversation and answer follow-up questions.

🚀 **What I can help with**:
- Analyze Python code for GPU optimization opportunities  
- Convert NumPy → CuPy, Pandas → cuDF, scikit-learn → cuML
- Explain GPU acceleration concepts and best practices
- Answer follow-up questions based on our conversation

Feel free to ask questions about GPU acceleration or paste code for analysis!"""
                }]
            
            def clear_code():
                return "", ""  # Clear both code input and optimized code
            
            def clear_execution_results():
                original_msg = "**Original Code Execution Results**\n\nClick '⚡ Benchmark on Sol' to execute the original code on the Sol supercomputer and see timing results."
                optimized_msg = "**GPU-Optimized Code Execution Results**\n\nClick '⚡ Benchmark on Sol' to execute the GPU-optimized code and compare performance."
                return original_msg, optimized_msg
            
            # Wire up the chat interface
            sample_dropdown.change(load_sample_code, inputs=[sample_dropdown], outputs=[code_input])
            load_sample_btn.click(load_sample_code, inputs=[sample_dropdown], outputs=[code_input])
            
            submit_btn.click(
                self.gpu_mentor.chat_interface,
                inputs=[message_input, code_input, chatbot],
                outputs=[message_input, code_input, chatbot]
            )
            
            message_input.submit(
                self.gpu_mentor.chat_interface,
                inputs=[message_input, code_input, chatbot],
                outputs=[message_input, code_input, chatbot]
            )
            
            clear_btn.click(clear_chat, outputs=[chatbot])
            
            # Wire up the code analysis interface
            analysis_sample_dropdown.change(load_sample_code, inputs=[analysis_sample_dropdown], outputs=[analyze_code])
            load_analysis_sample_btn.click(load_sample_code, inputs=[analysis_sample_dropdown], outputs=[analyze_code])
            clear_code_btn.click(clear_code, outputs=[analyze_code, optimized_code])
            clear_code_btn.click(clear_execution_results, outputs=[original_execution_output, optimized_execution_output])
            
            analyze_btn.click(
                self.gpu_mentor.analyze_code_only,
                inputs=[analyze_code],
                outputs=[analysis_results, optimized_code]
            )
            
            # Benchmark button already wired up above
            
            generate_tutorial_btn.click(
                self.gpu_mentor.get_tutorial_content,
                inputs=[tutorial_topic],
                outputs=[tutorial_content]
            )
            
            summary_btn.click(
                self.gpu_mentor.get_execution_summary,
                outputs=[execution_summary]
            )
        
        return interface
    
    def launch(self, share=True, **kwargs):
        """Launch the application with proper shutdown handling."""
        interface = self.create_interface()
        
        # Set default parameters for better control - let Gradio find an available port
        launch_params = {
            'share': share,
            'server_name': '0.0.0.0',
            'quiet': False,
            'show_error': True,
            'inbrowser': False,
            'prevent_thread_lock': False
        }
        
        # Override with any user-provided parameters
        launch_params.update(kwargs)
        
        try:
            interface.launch(**launch_params)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down Gradio interface...")
            interface.close()
            raise
        except Exception as e:
            print(f"❌ Error in Gradio interface: {e}")
            interface.close()
            raise
    
    def close(self):
        """Close the application gracefully."""
        print("🔄 Closing GPU Mentor application...")
        # Add any cleanup code here if needed

if __name__ == "__main__":
    app = GPUMentorApp()
    app.launch(share=True)
