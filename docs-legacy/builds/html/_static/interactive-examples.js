// Interactive Examples System for Haive Documentation
document.addEventListener("DOMContentLoaded", function () {
  console.log("🎮 Interactive Examples System loading...");

  // Cache for storing successful example runs
  const exampleCache = new Map();

  // Active running examples
  const runningExamples = new Set();

  class InteractiveExample {
    constructor(element) {
      this.element = element;
      this.exampleId = element.dataset.exampleId;
      this.module = element.dataset.module;
      this.type = element.dataset.type || "basic";
      this.cacheable = element.dataset.cacheable !== "false";
      this.setupUI();
    }

    setupUI() {
      const wrapper = document.createElement("div");
      wrapper.className = "interactive-example-wrapper";

      // Header with run button
      const header = document.createElement("div");
      header.className = "example-header";
      header.innerHTML = `
                <div class="example-info">
                    <span class="example-title">${this.getTitle()}</span>
                    <span class="example-module">${this.module}</span>
                </div>
                <div class="example-controls">
                    <button class="run-example-btn" ${this.isRunning() ? "disabled" : ""}>
                        ${this.getCachedResult() ? "▶️ Run Again" : "▶️ Run Example"}
                    </button>
                    <button class="toggle-code-btn">👁️ View Code</button>
                </div>
            `;

      // Code section (initially hidden)
      const codeSection = document.createElement("div");
      codeSection.className = "example-code-section hidden";
      const codeBlock = this.element.querySelector("pre, .highlight");
      if (codeBlock) {
        codeSection.appendChild(codeBlock.cloneNode(true));
      }

      // Output section
      const outputSection = document.createElement("div");
      outputSection.className = "example-output-section";

      // Check for cached result
      const cachedResult = this.getCachedResult();
      if (cachedResult) {
        outputSection.innerHTML = this.formatOutput(cachedResult);
      } else {
        outputSection.innerHTML =
          '<div class="output-placeholder">Click "Run Example" to see output</div>';
      }

      wrapper.appendChild(header);
      wrapper.appendChild(codeSection);
      wrapper.appendChild(outputSection);

      // Replace original element
      this.element.parentNode.replaceChild(wrapper, this.element);
      this.element = wrapper;

      this.bindEvents();
    }

    bindEvents() {
      const runBtn = this.element.querySelector(".run-example-btn");
      const toggleBtn = this.element.querySelector(".toggle-code-btn");
      const codeSection = this.element.querySelector(".example-code-section");

      runBtn.addEventListener("click", () => this.runExample());
      toggleBtn.addEventListener("click", () => {
        codeSection.classList.toggle("hidden");
        toggleBtn.textContent = codeSection.classList.contains("hidden")
          ? "👁️ View Code"
          : "🙈 Hide Code";
      });
    }

    getTitle() {
      const titles = {
        chess: "♟️ Chess Game Demo",
        tictactoe: "⭕ Tic-Tac-Toe Demo",
        connect4: "🔴 Connect4 Demo",
        simple: "🤖 Simple Agent Demo",
        rag: "📚 RAG Agent Demo",
        react: "🧠 ReAct Agent Demo",
      };
      return titles[this.type] || `🔧 ${this.module} Example`;
    }

    getCachedResult() {
      if (!this.cacheable) return null;
      return exampleCache.get(this.exampleId);
    }

    setCachedResult(result) {
      if (this.cacheable) {
        exampleCache.set(this.exampleId, result);
      }
    }

    isRunning() {
      return runningExamples.has(this.exampleId);
    }

    async runExample() {
      if (this.isRunning()) return;

      const runBtn = this.element.querySelector(".run-example-btn");
      const outputSection = this.element.querySelector(
        ".example-output-section",
      );

      // Set running state
      runningExamples.add(this.exampleId);
      runBtn.disabled = true;
      runBtn.innerHTML = "⏳ Running...";

      outputSection.innerHTML =
        '<div class="output-loading">🔄 Executing example...</div>';

      try {
        const result = await this.executeExample();
        this.setCachedResult(result);
        outputSection.innerHTML = this.formatOutput(result);
        runBtn.innerHTML = "▶️ Run Again";
      } catch (error) {
        console.error("Example execution failed:", error);
        outputSection.innerHTML = this.formatError(error);
        runBtn.innerHTML = "❌ Error - Try Again";
      } finally {
        runningExamples.delete(this.exampleId);
        runBtn.disabled = false;
      }
    }

    async executeExample() {
      // Mock execution for now - in real implementation this would call the Python backend
      return new Promise((resolve) => {
        setTimeout(
          () => {
            const mockResults = this.getMockResult();
            resolve(mockResults);
          },
          2000 + Math.random() * 3000,
        ); // 2-5 seconds
      });
    }

    getMockResult() {
      const mockResults = {
        chess: {
          type: "game",
          status: "completed",
          moves: [
            "e2-e4",
            "e7-e5",
            "Ng1-f3",
            "Nb8-c6",
            "Bf1-c4",
            "Bf8-c5",
            "O-O",
            "Ng8-f6",
          ],
          finalPosition:
            "rnbqk2r/pppp1ppp/5n2/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQ1RK1",
          result: "Game in progress",
          analysis: {
            white_advantage: "+0.3",
            key_moves: ["e2-e4 (King's Pawn opening)", "Bf1-c4 (Italian Game)"],
            position_summary:
              "Classical opening development. White has slight initiative.",
          },
          ui_output: `
┌───┬───┬───┬───┬───┬───┬───┬───┐
│ ♜ │ ♞ │ ♝ │ ♛ │ ♚ │   │   │ ♜ │ 8
├───┼───┼───┼───┼───┼───┼───┼───┤
│ ♟ │ ♟ │ ♟ │ ♟ │   │ ♟ │ ♟ │ ♟ │ 7
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │ ♞ │   │   │ 6
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │ ♝ │   │ ♟ │   │   │   │ 5
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │ ♗ │   │ ♙ │   │   │   │ 4
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │ ♘ │   │   │ 3
├───┼───┼───┼───┼───┼───┼───┼───┤
│ ♙ │ ♙ │ ♙ │ ♙ │   │ ♙ │ ♙ │ ♙ │ 2
├───┼───┼───┼───┼───┼───┼───┼───┤
│ ♖ │ ♘ │ ♗ │ ♕ │   │ ♖ │ ♔ │   │ 1
└───┴───┴───┴───┴───┴───┴───┴───┘
  a   b   c   d   e   f   g   h

🎯 Analysis: Classical Italian Game opening
📊 Position Eval: +0.3 (slight white advantage)
⏱️ Moves played: 8 | Time: 0:02:34
                    `,
        },
        simple: {
          type: "conversation",
          status: "completed",
          messages: [
            { role: "user", content: "Hello! How can you help me today?" },
            {
              role: "assistant",
              content:
                "Hello! I'm a Haive SimpleAgent. I can help you with various tasks including answering questions, providing information, and having conversations. What would you like to know or discuss?",
            },
          ],
          metadata: {
            model: "gpt-4o",
            tokens_used: 156,
            response_time: "1.2s",
          },
        },
        rag: {
          type: "retrieval",
          status: "completed",
          query: "How do I create a chess agent?",
          retrieved_docs: [
            {
              source: "chess/README.md",
              relevance: 0.95,
              snippet:
                "ChessAgent is the main class for creating AI chess players...",
            },
            {
              source: "agents/base.py",
              relevance: 0.87,
              snippet:
                "The Agent base class provides the foundation for all agents...",
            },
          ],
          response:
            "To create a chess agent, you can use the ChessAgent class from haive.games.chess. Here's how to get started...",
          metadata: {
            retrieval_time: "0.3s",
            generation_time: "2.1s",
            total_docs: 234,
            retrieved_docs: 5,
          },
        },
      };
      return mockResults[this.type] || mockResults["simple"];
    }

    formatOutput(result) {
      if (result.type === "game") {
        return `
                    <div class="game-output">
                        <div class="game-header">
                            <span class="game-status ${result.status}">${result.status.toUpperCase()}</span>
                            <span class="game-result">${result.result}</span>
                        </div>

                        <div class="game-board">
                            <pre class="board-display">${result.ui_output}</pre>
                        </div>

                        <div class="game-info">
                            <div class="moves-section">
                                <h4>📝 Move History</h4>
                                <div class="moves-list">
                                    ${result.moves
                                      .map(
                                        (move, i) =>
                                          `<span class="move">${Math.floor(i / 2) + 1}${i % 2 === 0 ? "." : "..."} ${move}</span>`,
                                      )
                                      .join(" ")}
                                </div>
                            </div>

                            <div class="analysis-section">
                                <h4>🧠 AI Analysis</h4>
                                <div class="analysis-content">
                                    <p><strong>Position:</strong> ${result.analysis.position_summary}</p>
                                    <p><strong>Evaluation:</strong> ${result.analysis.white_advantage}</p>
                                    <div class="key-moves">
                                        <strong>Key Moves:</strong>
                                        <ul>
                                            ${result.analysis.key_moves.map((move) => `<li>${move}</li>`).join("")}
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
      } else if (result.type === "conversation") {
        return `
                    <div class="conversation-output">
                        <div class="messages">
                            ${result.messages
                              .map(
                                (msg) => `
                                <div class="message ${msg.role}">
                                    <div class="message-header">${msg.role === "user" ? "👤 User" : "🤖 Agent"}</div>
                                    <div class="message-content">${msg.content}</div>
                                </div>
                            `,
                              )
                              .join("")}
                        </div>
                        <div class="metadata">
                            <span>Model: ${result.metadata.model}</span>
                            <span>Tokens: ${result.metadata.tokens_used}</span>
                            <span>Time: ${result.metadata.response_time}</span>
                        </div>
                    </div>
                `;
      } else if (result.type === "retrieval") {
        return `
                    <div class="rag-output">
                        <div class="query-section">
                            <h4>❓ Query</h4>
                            <p class="query">${result.query}</p>
                        </div>

                        <div class="retrieval-section">
                            <h4>📚 Retrieved Documents</h4>
                            <div class="docs-list">
                                ${result.retrieved_docs
                                  .map(
                                    (doc) => `
                                    <div class="doc-item">
                                        <div class="doc-header">
                                            <span class="doc-source">${doc.source}</span>
                                            <span class="doc-relevance">${(doc.relevance * 100).toFixed(1)}%</span>
                                        </div>
                                        <div class="doc-snippet">${doc.snippet}</div>
                                    </div>
                                `,
                                  )
                                  .join("")}
                            </div>
                        </div>

                        <div class="response-section">
                            <h4>💬 Generated Response</h4>
                            <p class="response">${result.response}</p>
                        </div>

                        <div class="metadata">
                            <span>Retrieval: ${result.metadata.retrieval_time}</span>
                            <span>Generation: ${result.metadata.generation_time}</span>
                            <span>Retrieved: ${result.metadata.retrieved_docs}/${result.metadata.total_docs} docs</span>
                        </div>
                    </div>
                `;
      }

      return `<div class="simple-output"><pre>${JSON.stringify(result, null, 2)}</pre></div>`;
    }

    formatError(error) {
      return `
                <div class="error-output">
                    <div class="error-header">❌ Execution Error</div>
                    <div class="error-message">${error.message || error}</div>
                    <div class="error-help">
                        <p>This might be due to:</p>
                        <ul>
                            <li>Missing dependencies</li>
                            <li>Network connectivity issues</li>
                            <li>API rate limits</li>
                        </ul>
                        <p>Try running the example again or check the console for more details.</p>
                    </div>
                </div>
            `;
    }
  }

  // Initialize all interactive examples on the page
  function initializeExamples() {
    const examples = document.querySelectorAll(".interactive-example");
    examples.forEach((element) => new InteractiveExample(element));
  }

  // Auto-initialize
  initializeExamples();

  // Export for manual initialization
  window.InteractiveExample = InteractiveExample;
  window.initializeExamples = initializeExamples;

  console.log("✅ Interactive Examples System loaded");
});
