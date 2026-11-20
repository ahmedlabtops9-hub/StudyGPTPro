create table if not exists public.study_progress (
  user_email text primary key,
  data jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

create or replace function public.set_study_progress_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists study_progress_updated_at on public.study_progress;
create trigger study_progress_updated_at
before update on public.study_progress
for each row execute function public.set_study_progress_updated_at();

alter table public.study_progress enable row level security;

-- The app accesses this table server-side using the Supabase service role key.
-- Never expose the service role key in client-side code or public repositories.
