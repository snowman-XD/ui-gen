# ui-gen
<pre>
    graph TD
    subgraph Input_Layer [User Input]
        A[📸 UI Screenshot/Mockup]
    end

    subgraph AI_Engine [Intelligence Layer]
        B[🧠 LLM Vision Analysis]
        C[🛠️ Component Mapping]
        D[📝 Code Synthesis]
        B --&gt; C --&gt; D
    end

    subgraph DevOps_Pipeline [Deployment Engine]
        E[🐙 GitHub Repository]
        F[🏗️ CI/CD Build]
        G[🚀 Production Server]
        E --&gt; F --&gt; G
    end

    %% Connection Logic
    A --&gt; B
    D --&gt;|Git Commit| E
    G --&gt; H([🌐 Live URL])

    %% Styling
    style B fill:#6366f1,color:#fff
    style D fill:#6366f1,color:#fff
    style H fill:#22c55e,color:#fff
    style A fill:#f59e0b,color:#fff
</pre>
uploaded screenshot <img width="1920" height="1080" alt="af8ebf7da9c1f28a35f0ff230a3427ecaeddc803" src="https://github.com/user-attachments/assets/475d5af0-3dfc-4c00-8c40-6f6e40c7dafd" />
output produced by ui generator <img width="1467" height="744" alt="Screenshot 2026-02-25 at 8 51 51 AM" src="https://github.com/user-attachments/assets/263742f0-7954-4f9d-9401-941dfdf5b10b" />
