-- Tabla para almacenar los perfiles de usuario y sus límites
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    subscription_tier TEXT DEFAULT 'free',
    research_credits INTEGER DEFAULT 5,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla para almacenar el historial de investigaciones
CREATE TABLE IF NOT EXISTS public.researches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    topic TEXT NOT NULL,
    status TEXT DEFAULT 'completed',
    result TEXT, -- El reporte en formato Markdown
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Habilitar Row Level Security (RLS) para mayor seguridad
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.researches ENABLE ROW LEVEL SECURITY;

-- Crear políticas básicas (simplificadas para desarrollo)
CREATE POLICY "Users can see their own profile" ON public.users FOR SELECT USING (true);
CREATE POLICY "Users can see their own researches" ON public.researches FOR SELECT USING (true);
CREATE POLICY "Users can insert their own researches" ON public.researches FOR INSERT WITH CHECK (true);
