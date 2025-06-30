-- Supabase Schema Setup for Haive
-- This creates the proper table structure that integrates with auth.users
-- and mimics your local PostgreSQL setup

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ===========================================
-- USER PROFILES TABLE (mirrors your local setup)
-- ===========================================

-- Create user profiles table linked to auth.users
CREATE TABLE IF NOT EXISTS public.user_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    username TEXT UNIQUE,
    full_name TEXT,
    email TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    preferences JSONB DEFAULT '{}'
);

-- Enable RLS for user profiles
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;

-- RLS policies for user profiles
CREATE POLICY "Users can view own profile" ON public.user_profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.user_profiles
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" ON public.user_profiles
    FOR INSERT WITH CHECK (auth.uid() = id);

-- Trigger to auto-create user profile when auth.users record is created
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.user_profiles (id, email, username, full_name)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'username', NEW.email),
        COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.email)
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ===========================================
-- THREADS TABLE (mimics your local structure)
-- ===========================================

-- Create threads table with proper auth integration
CREATE TABLE IF NOT EXISTS public.threads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    thread_id TEXT UNIQUE NOT NULL DEFAULT uuid_generate_v4()::text, -- For backwards compatibility
    agent_name TEXT NOT NULL DEFAULT 'Unknown Agent',
    name TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_access TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'archived', 'deleted'))
);

-- Enable RLS for threads
ALTER TABLE public.threads ENABLE ROW LEVEL SECURITY;

-- RLS policies for threads
CREATE POLICY "Users can view own threads" ON public.threads
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own threads" ON public.threads
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own threads" ON public.threads
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own threads" ON public.threads
    FOR DELETE USING (auth.uid() = user_id);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_threads_user_id ON public.threads(user_id);
CREATE INDEX IF NOT EXISTS idx_threads_thread_id ON public.threads(thread_id);
CREATE INDEX IF NOT EXISTS idx_threads_user_created ON public.threads(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_threads_status ON public.threads(status);

-- ===========================================
-- ENHANCED CHECKPOINTS TABLE (integrates with your local setup)
-- ===========================================

-- Create enhanced checkpoints table that works with LangGraph but adds user context
CREATE TABLE IF NOT EXISTS public.enhanced_checkpoints (
    thread_id TEXT NOT NULL,
    checkpoint_ns TEXT NOT NULL DEFAULT '',
    checkpoint_id TEXT NOT NULL,
    parent_checkpoint_id TEXT,
    type TEXT,
    checkpoint JSONB NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    -- Enhanced fields for user integration
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    thread_uuid UUID REFERENCES public.threads(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id)
);

-- Enable RLS for enhanced checkpoints
ALTER TABLE public.enhanced_checkpoints ENABLE ROW LEVEL SECURITY;

-- RLS policies for enhanced checkpoints
CREATE POLICY "Users can access own checkpoints" ON public.enhanced_checkpoints
    FOR ALL USING (auth.uid() = user_id);

-- Indexes for checkpoints
CREATE INDEX IF NOT EXISTS idx_enhanced_checkpoints_user_thread ON public.enhanced_checkpoints(user_id, thread_id);
CREATE INDEX IF NOT EXISTS idx_enhanced_checkpoints_thread_ns ON public.enhanced_checkpoints(thread_id, checkpoint_ns);
CREATE INDEX IF NOT EXISTS idx_enhanced_checkpoints_user_created ON public.enhanced_checkpoints(user_id, created_at DESC);

-- ===========================================
-- CHECKPOINT BLOBS TABLE (for large data)
-- ===========================================

CREATE TABLE IF NOT EXISTS public.enhanced_checkpoint_blobs (
    thread_id TEXT NOT NULL,
    checkpoint_ns TEXT NOT NULL DEFAULT '',
    channel TEXT NOT NULL,
    version TEXT NOT NULL,
    type TEXT NOT NULL,
    blob BYTEA,
    -- Enhanced fields
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (thread_id, checkpoint_ns, channel, version)
);

-- Enable RLS for checkpoint blobs
ALTER TABLE public.enhanced_checkpoint_blobs ENABLE ROW LEVEL SECURITY;

-- RLS policies for checkpoint blobs
CREATE POLICY "Users can access own checkpoint blobs" ON public.enhanced_checkpoint_blobs
    FOR ALL USING (auth.uid() = user_id);

-- ===========================================
-- CHECKPOINT WRITES TABLE (for pending writes)
-- ===========================================

CREATE TABLE IF NOT EXISTS public.enhanced_checkpoint_writes (
    thread_id TEXT NOT NULL,
    checkpoint_ns TEXT NOT NULL DEFAULT '',
    checkpoint_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    idx INTEGER NOT NULL,
    channel TEXT NOT NULL,
    type TEXT,
    blob BYTEA NOT NULL,
    task_path TEXT NOT NULL DEFAULT '',
    -- Enhanced fields
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id, task_id, idx)
);

-- Enable RLS for checkpoint writes
ALTER TABLE public.enhanced_checkpoint_writes ENABLE ROW LEVEL SECURITY;

-- RLS policies for checkpoint writes
CREATE POLICY "Users can access own checkpoint writes" ON public.enhanced_checkpoint_writes
    FOR ALL USING (auth.uid() = user_id);

-- ===========================================
-- THREAD MANAGEMENT FUNCTIONS
-- ===========================================

-- Function to register a new thread (mimics your local function)
CREATE OR REPLACE FUNCTION public.register_thread(
    p_user_id UUID,
    p_thread_id TEXT DEFAULT NULL,
    p_agent_name TEXT DEFAULT 'Unknown Agent',
    p_name TEXT DEFAULT NULL,
    p_metadata JSONB DEFAULT '{}'
) RETURNS UUID AS $$
DECLARE
    v_thread_uuid UUID;
    v_thread_id TEXT;
BEGIN
    -- Generate thread_id if not provided
    v_thread_id := COALESCE(p_thread_id, uuid_generate_v4()::text);
    
    -- Insert or update thread
    INSERT INTO public.threads (user_id, thread_id, agent_name, name, metadata)
    VALUES (p_user_id, v_thread_id, p_agent_name, p_name, p_metadata)
    ON CONFLICT (thread_id) 
    DO UPDATE SET
        updated_at = NOW(),
        last_access = NOW(),
        agent_name = EXCLUDED.agent_name,
        name = COALESCE(EXCLUDED.name, threads.name),
        metadata = threads.metadata || EXCLUDED.metadata
    RETURNING id INTO v_thread_uuid;
    
    RETURN v_thread_uuid;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to get user threads
CREATE OR REPLACE FUNCTION public.get_user_threads(
    p_user_id UUID DEFAULT NULL,
    p_limit INTEGER DEFAULT 50,
    p_offset INTEGER DEFAULT 0
) RETURNS TABLE (
    id UUID,
    thread_id TEXT,
    agent_name TEXT,
    name TEXT,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    last_access TIMESTAMPTZ,
    metadata JSONB,
    status TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        t.id,
        t.thread_id,
        t.agent_name,
        t.name,
        t.created_at,
        t.updated_at,
        t.last_access,
        t.metadata,
        t.status
    FROM public.threads t
    WHERE t.user_id = COALESCE(p_user_id, auth.uid())
    AND t.status = 'active'
    ORDER BY t.last_access DESC
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to update thread access time
CREATE OR REPLACE FUNCTION public.update_thread_access(p_thread_id TEXT)
RETURNS VOID AS $$
BEGIN
    UPDATE public.threads 
    SET last_access = NOW()
    WHERE thread_id = p_thread_id 
    AND user_id = auth.uid();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ===========================================
-- HELPER FUNCTIONS FOR AUTH CONTEXT
-- ===========================================

-- Function to set user context for RLS (useful for server-side operations)
CREATE OR REPLACE FUNCTION public.set_user_context(p_user_id UUID)
RETURNS VOID AS $$
BEGIN
    PERFORM set_config('request.jwt.claims', json_build_object('sub', p_user_id)::text, true);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to get current user context
CREATE OR REPLACE FUNCTION public.get_current_user_id()
RETURNS UUID AS $$
BEGIN
    RETURN auth.uid();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ===========================================
-- MIGRATION HELPERS
-- ===========================================

-- Function to migrate existing threads from standard checkpoints table
CREATE OR REPLACE FUNCTION public.migrate_existing_threads()
RETURNS INTEGER AS $$
DECLARE
    v_count INTEGER := 0;
    v_record RECORD;
BEGIN
    -- Migrate unique threads from existing checkpoints table if it exists
    FOR v_record IN 
        SELECT DISTINCT thread_id
        FROM public.checkpoints 
        WHERE thread_id IS NOT NULL
    LOOP
        -- Try to register the thread (will skip if already exists)
        PERFORM public.register_thread(
            p_user_id := '00000000-0000-0000-0000-000000000000'::UUID, -- Default user
            p_thread_id := v_record.thread_id,
            p_agent_name := 'Migrated Agent'
        );
        v_count := v_count + 1;
    END LOOP;
    
    RETURN v_count;
EXCEPTION 
    WHEN OTHERS THEN
        -- Ignore errors if checkpoints table doesn't exist
        RETURN 0;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ===========================================
-- VIEWS FOR EASY QUERYING
-- ===========================================

-- View that combines threads with checkpoint statistics
CREATE OR REPLACE VIEW public.thread_stats AS
SELECT 
    t.id,
    t.thread_id,
    t.user_id,
    t.agent_name,
    t.name,
    t.created_at,
    t.updated_at,
    t.last_access,
    t.metadata,
    t.status,
    COALESCE(c.checkpoint_count, 0) as checkpoint_count,
    c.last_checkpoint_at
FROM public.threads t
LEFT JOIN (
    SELECT 
        thread_id,
        COUNT(*) as checkpoint_count,
        MAX(created_at) as last_checkpoint_at
    FROM public.enhanced_checkpoints
    GROUP BY thread_id
) c ON t.thread_id = c.thread_id;

-- Enable RLS on the view
ALTER VIEW public.thread_stats SET (security_invoker = true);

-- ===========================================
-- GRANTS AND PERMISSIONS
-- ===========================================

-- Grant necessary permissions to authenticated users
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT ALL ON public.user_profiles TO authenticated;
GRANT ALL ON public.threads TO authenticated;
GRANT ALL ON public.enhanced_checkpoints TO authenticated;
GRANT ALL ON public.enhanced_checkpoint_blobs TO authenticated;
GRANT ALL ON public.enhanced_checkpoint_writes TO authenticated;
GRANT SELECT ON public.thread_stats TO authenticated;

-- Grant execute permissions on functions
GRANT EXECUTE ON FUNCTION public.register_thread TO authenticated;
GRANT EXECUTE ON FUNCTION public.get_user_threads TO authenticated;
GRANT EXECUTE ON FUNCTION public.update_thread_access TO authenticated;
GRANT EXECUTE ON FUNCTION public.get_current_user_id TO authenticated;

-- ===========================================
-- COMPLETION MESSAGE
-- ===========================================

-- Log successful completion
DO $$
BEGIN
    RAISE NOTICE 'Haive Supabase schema setup completed successfully!';
    RAISE NOTICE 'Tables created: user_profiles, threads, enhanced_checkpoints, enhanced_checkpoint_blobs, enhanced_checkpoint_writes';
    RAISE NOTICE 'All tables have Row Level Security enabled';
    RAISE NOTICE 'Helper functions created for thread management';
    RAISE NOTICE 'Ready for integration with auth.users';
END $$;