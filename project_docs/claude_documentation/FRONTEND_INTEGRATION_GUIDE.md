# Haive Enhanced Streaming & Supabase Integration Guide

## 🎉 Migration Complete!

Your Haive backend has been successfully upgraded with:

- **Enhanced agent streaming** with multiple modes and formats
- **Supabase integration** for persistent agent conversations
- **Fixed authentication** with proper JWT validation

---

## 🔧 Backend Configuration

### API Endpoints

- **Base URL**: `http://192.168.2.13:8000`
- **Health Check**: `GET /api/health`
- **LLM Generate**: `POST /api/llm/generate?query=your_query`
- **Agent WebSocket**: `ws://192.168.2.13:8000/api/ws/chat/{agent_name}`

### Authentication

- **JWT Token Required**: Use Supabase JWT tokens
- **Header**: `Authorization: Bearer YOUR_JWT_TOKEN`
- **User ID**: Extracted from JWT `sub` field

---

## 🚀 Enhanced Streaming Configuration

### WebSocket URL Format

```
ws://192.168.2.13:8000/api/ws/chat/{agent_name}?token={jwt_token}&config={json_config}
```

### Streaming Configuration Options

```typescript
interface AgentStreamConfig {
  agent_name: string; // Name of the agent
  provider: "azure" | "openai" | "anthropic"; // LLM provider
  model: string; // Model name (e.g., "gpt-4o")
  stream: boolean; // Enable/disable streaming
  persistent: boolean; // Save to Supabase

  // New enhanced options:
  stream_mode: "messages" | "values" | "updates" | "debug" | "custom";
  stream_format: "auto" | "json" | "text" | "structured";
  progressive_updates: boolean; // Send partial results
  buffer_chunks: boolean; // Buffer multiple chunks
  chunk_size: number; // Buffer size (if buffering enabled)
}
```

### Stream Modes Explained

#### 1. **Messages Mode** (`stream_mode: "messages"`)

- **Best for**: Chat interfaces
- **Returns**: Individual message content
- **Format options**:
  - `"text"`: Just the text content
  - `"json"`: Full message objects

#### 2. **Values Mode** (`stream_mode: "values"`)

- **Best for**: State-based applications
- **Returns**: Complete state values
- **Format options**:
  - `"structured"`: Include type information
  - `"json"`: Raw JSON data

#### 3. **Updates Mode** (`stream_mode: "updates"`)

- **Best for**: Real-time progress tracking
- **Returns**: Only changes/updates
- **Format options**:
  - `"structured"`: Changes with metadata

#### 4. **Debug Mode** (`stream_mode: "debug"`)

- **Best for**: Development and debugging
- **Returns**: Detailed execution information

---

## 💾 Supabase Integration

### Database Schema

Your conversations are now stored in Supabase with the following structure:

#### Tables Created:

- `agent_state.threads` - Conversation threads
- `agent_state.checkpoints` - Agent state snapshots
- `agent_state.conversations` - Message history
- `agent_state.agent_configs` - Agent configurations
- `agent_state.agent_metrics` - Usage metrics

#### Row Level Security (RLS)

- ✅ Users can only access their own data
- ✅ Automatic user isolation based on JWT
- ✅ Secure multi-tenant architecture

---

## 📱 Frontend Integration Examples

### 1. Basic Chat Streaming

```typescript
const config = {
  agent_name: "ChatAgent",
  provider: "azure",
  model: "gpt-4o",
  stream: true,
  stream_mode: "messages",
  stream_format: "text",
  persistent: true, // Save to Supabase
};

const wsUrl = `ws://192.168.2.13:8000/api/ws/chat/ChatAgent?token=${userToken}&config=${JSON.stringify(config)}`;

const websocket = new WebSocket(wsUrl);

websocket.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.type === "response") {
    // Stream text content
    appendToChat(data.content);
  } else if (data.type === "status") {
    if (data.content.status === "complete") {
      console.log("Stream complete");
    }
  }
};
```

### 2. Structured Data Streaming

```typescript
const config = {
  agent_name: "AnalysisAgent",
  stream_mode: "values",
  stream_format: "structured",
  progressive_updates: true,
};

websocket.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.type === "response") {
    const structuredData = data.content;

    if (structuredData.valid) {
      // Use validated structured data
      updateAnalysisDisplay(structuredData.data);
    }
  }
};
```

### 3. Real-time Progress Updates

```typescript
const config = {
  stream_mode: "updates",
  stream_format: "json",
  buffer_chunks: false, // Immediate delivery
};

websocket.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.type === "response") {
    // Real-time updates
    updateProgressBar(data.content);
  }
};
```

---

## 🗄️ Supabase Database Access

### Direct Database Queries (Optional)

You can also query conversation history directly from Supabase:

```typescript
// Get user's conversation threads
const { data: threads } = await supabase
  .from("agent_state.threads")
  .select("*")
  .eq("user_id", userId)
  .order("updated_at", { ascending: false });

// Get conversation messages
const { data: messages } = await supabase
  .from("agent_state.conversations")
  .select("*")
  .eq("thread_id", threadId)
  .order("created_at", { ascending: true });
```

---

## 🛠️ Configuration Examples by Use Case

### Chat Application

```typescript
{
  stream_mode: "messages",
  stream_format: "text",
  persistent: true,
  buffer_chunks: false
}
```

### Data Analysis Dashboard

```typescript
{
  stream_mode: "values",
  stream_format: "structured",
  progressive_updates: true,
  persistent: true
}
```

### Real-time Collaboration

```typescript
{
  stream_mode: "updates",
  stream_format: "json",
  buffer_chunks: false,
  persistent: true
}
```

### Development/Testing

```typescript
{
  stream_mode: "debug",
  stream_format: "json",
  persistent: false
}
```

---

## 🔐 Security Notes

1. **JWT Tokens**: Always use valid Supabase JWT tokens
2. **User Isolation**: Data is automatically isolated by user ID
3. **CORS**: Configured to accept requests from your frontend
4. **Rate Limiting**: 60 requests per minute per user

---

## 📊 Monitoring & Debugging

### Health Check

```bash
curl http://192.168.2.13:8000/api/health
```

### View Logs

- Server logs available at `/tmp/haive_api.log`
- Check Supabase dashboard for database activity

---

## 🚨 Troubleshooting

### Common Issues:

1. **WebSocket Connection Refused**
   - Check if API server is running
   - Verify JWT token is valid and not expired

2. **Authentication Errors**
   - Ensure JWT token is in `Authorization` header
   - Check token format: `Bearer YOUR_TOKEN`

3. **Missing Data in Supabase**
   - Verify `persistent: true` in config
   - Check RLS policies are applied correctly

---

## 📞 Support

If you encounter any issues:

1. Check the server logs at `/tmp/haive_api.log`
2. Verify Supabase dashboard shows incoming data
3. Test with the provided examples first

The backend is now production-ready with enhanced streaming and persistent storage! 🎉
