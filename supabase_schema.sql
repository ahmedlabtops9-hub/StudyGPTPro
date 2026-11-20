-- StudyGPT Pro: core learning platform schema
-- Apply in Supabase SQL editor. Auth identities are managed by Supabase Auth.

create extension if not exists pgcrypto;

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text not null default '',
  phone text,
  stage text not null default 'first_baccalaureate'
    check (stage in ('first_baccalaureate','second_baccalaureate')),
  role text not null default 'student'
    check (role in ('student','teacher','admin')),
  school_days jsonb not null default '[]'::jsonb,
  timezone text not null default 'Africa/Cairo',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.subjects (
  id uuid primary key default gen_random_uuid(),
  stage text not null check (stage in ('first_baccalaureate','second_baccalaureate')),
  name text not null,
  description text not null default '',
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  unique(stage, name)
);

create table if not exists public.study_materials (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references public.profiles(id) on delete cascade,
  subject_id uuid references public.subjects(id) on delete set null,
  title text not null,
  material_type text not null default 'note'
    check (material_type in ('note','pdf','document','link','video')),
  storage_path text,
  source_url text,
  extracted_text text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.study_sessions (
  id uuid primary key default gen_random_uuid(),
  student_id uuid not null references public.profiles(id) on delete cascade,
  subject_id uuid references public.subjects(id) on delete set null,
  title text not null,
  starts_at timestamptz not null,
  duration_minutes integer not null default 60 check (duration_minutes between 5 and 600),
  location text,
  reminder_minutes integer not null default 30 check (reminder_minutes between 0 and 1440),
  recurrence jsonb not null default '{}'::jsonb,
  status text not null default 'scheduled'
    check (status in ('scheduled','completed','cancelled')),
  created_at timestamptz not null default now()
);

create table if not exists public.study_tasks (
  id uuid primary key default gen_random_uuid(),
  student_id uuid not null references public.profiles(id) on delete cascade,
  subject_id uuid references public.subjects(id) on delete set null,
  title text not null,
  details text not null default '',
  due_at timestamptz,
  estimated_minutes integer check (estimated_minutes is null or estimated_minutes between 1 and 1440),
  priority text not null default 'normal' check (priority in ('low','normal','high')),
  status text not null default 'todo' check (status in ('todo','doing','done')),
  source text not null default 'student' check (source in ('student','assistant','teacher')),
  created_at timestamptz not null default now(),
  completed_at timestamptz
);

create table if not exists public.ai_conversations (
  id uuid primary key default gen_random_uuid(),
  student_id uuid not null references public.profiles(id) on delete cascade,
  subject_id uuid references public.subjects(id) on delete set null,
  title text not null default 'محادثة جديدة',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.ai_messages (
  id uuid primary key default gen_random_uuid(),
  conversation_id uuid not null references public.ai_conversations(id) on delete cascade,
  role text not null check (role in ('user','assistant','system')),
  content text not null,
  citations jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.quizzes (
  id uuid primary key default gen_random_uuid(),
  creator_id uuid not null references public.profiles(id) on delete cascade,
  subject_id uuid references public.subjects(id) on delete set null,
  title text not null,
  description text not null default '',
  stage text not null check (stage in ('first_baccalaureate','second_baccalaureate')),
  question_count integer not null default 10 check (question_count >= 10),
  duration_minutes integer check (duration_minutes is null or duration_minutes > 0),
  is_published boolean not null default false,
  availability_start timestamptz,
  availability_end timestamptz,
  created_at timestamptz not null default now()
);

create table if not exists public.quiz_questions (
  id uuid primary key default gen_random_uuid(),
  quiz_id uuid not null references public.quizzes(id) on delete cascade,
  position integer not null,
  question_type text not null check (question_type in ('mcq','true_false','short_answer','essay')),
  prompt text not null,
  choices jsonb not null default '[]'::jsonb,
  answer_key jsonb,
  explanation text not null default '',
  points numeric(7,2) not null default 1 check (points > 0),
  difficulty text not null default 'medium' check (difficulty in ('easy','medium','hard')),
  unique(quiz_id, position)
);

create table if not exists public.quiz_assignments (
  id uuid primary key default gen_random_uuid(),
  quiz_id uuid not null references public.quizzes(id) on delete cascade,
  student_id uuid not null references public.profiles(id) on delete cascade,
  assigned_by uuid not null references public.profiles(id) on delete cascade,
  due_at timestamptz,
  created_at timestamptz not null default now(),
  unique(quiz_id, student_id)
);

create table if not exists public.quiz_attempts (
  id uuid primary key default gen_random_uuid(),
  quiz_id uuid not null references public.quizzes(id) on delete cascade,
  student_id uuid not null references public.profiles(id) on delete cascade,
  started_at timestamptz not null default now(),
  submitted_at timestamptz,
  auto_score numeric(8,2),
  teacher_score numeric(8,2),
  max_score numeric(8,2),
  grading_status text not null default 'pending'
    check (grading_status in ('pending','auto_graded','teacher_reviewed')),
  teacher_feedback text,
  integrity_events jsonb not null default '[]'::jsonb
);

create table if not exists public.quiz_answers (
  id uuid primary key default gen_random_uuid(),
  attempt_id uuid not null references public.quiz_attempts(id) on delete cascade,
  question_id uuid not null references public.quiz_questions(id) on delete cascade,
  answer jsonb not null default 'null'::jsonb,
  awarded_points numeric(8,2),
  feedback text not null default '',
  graded_by uuid references public.profiles(id) on delete set null,
  unique(attempt_id, question_id)
);

create table if not exists public.teacher_groups (
  id uuid primary key default gen_random_uuid(),
  teacher_id uuid not null references public.profiles(id) on delete cascade,
  title text not null,
  description text not null default '',
  join_code text not null unique default upper(substr(encode(gen_random_bytes(8),'hex'),1,10)),
  is_active boolean not null default true,
  created_at timestamptz not null default now()
);

create table if not exists public.group_members (
  group_id uuid not null references public.teacher_groups(id) on delete cascade,
  student_id uuid not null references public.profiles(id) on delete cascade,
  joined_at timestamptz not null default now(),
  primary key(group_id, student_id)
);

create table if not exists public.student_mastery (
  id uuid primary key default gen_random_uuid(),
  student_id uuid not null references public.profiles(id) on delete cascade,
  subject_id uuid not null references public.subjects(id) on delete cascade,
  skill_key text not null,
  skill_title text not null,
  mastery_score numeric(5,2) not null default 0 check (mastery_score between 0 and 100),
  confidence text not null default 'unknown'
    check (confidence in ('unknown','weak','developing','strong')),
  last_assessed_at timestamptz,
  evidence jsonb not null default '[]'::jsonb,
  unique(student_id, subject_id, skill_key)
);

create table if not exists public.notifications (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.profiles(id) on delete cascade,
  title text not null,
  body text not null,
  channel text not null default 'in_app' check (channel in ('in_app','email','sms','push')),
  scheduled_for timestamptz,
  sent_at timestamptz,
  read_at timestamptz,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists study_sessions_student_start_idx on public.study_sessions(student_id, starts_at);
create index if not exists study_tasks_student_due_idx on public.study_tasks(student_id, due_at);
create index if not exists ai_conversations_student_updated_idx on public.ai_conversations(student_id, updated_at desc);
create index if not exists ai_messages_conversation_created_idx on public.ai_messages(conversation_id, created_at);
create index if not exists quiz_attempts_student_submitted_idx on public.quiz_attempts(student_id, submitted_at desc);
create index if not exists notifications_user_schedule_idx on public.notifications(user_id, scheduled_for);

-- Enable row-level security on all student and teacher data.
alter table public.profiles enable row level security;
alter table public.subjects enable row level security;
alter table public.study_materials enable row level security;
alter table public.study_sessions enable row level security;
alter table public.study_tasks enable row level security;
alter table public.ai_conversations enable row level security;
alter table public.ai_messages enable row level security;
alter table public.quizzes enable row level security;
alter table public.quiz_questions enable row level security;
alter table public.quiz_assignments enable row level security;
alter table public.quiz_attempts enable row level security;
alter table public.quiz_answers enable row level security;
alter table public.teacher_groups enable row level security;
alter table public.group_members enable row level security;
alter table public.student_mastery enable row level security;
alter table public.notifications enable row level security;

-- Students own their personal records. Teacher access is granted through group membership
-- in server-side authorization logic; never trust a client-supplied role.
drop policy if exists profiles_select_own on public.profiles;
create policy profiles_select_own on public.profiles for select using (id = auth.uid());
drop policy if exists profiles_update_own on public.profiles;
create policy profiles_update_own on public.profiles for update using (id = auth.uid()) with check (id = auth.uid());

drop policy if exists subjects_read_active on public.subjects;
create policy subjects_read_active on public.subjects for select using (is_active = true);

drop policy if exists materials_owner_all on public.study_materials;
create policy materials_owner_all on public.study_materials for all using (owner_id = auth.uid()) with check (owner_id = auth.uid());
drop policy if exists sessions_owner_all on public.study_sessions;
create policy sessions_owner_all on public.study_sessions for all using (student_id = auth.uid()) with check (student_id = auth.uid());
drop policy if exists tasks_owner_all on public.study_tasks;
create policy tasks_owner_all on public.study_tasks for all using (student_id = auth.uid()) with check (student_id = auth.uid());
drop policy if exists conversations_owner_all on public.ai_conversations;
create policy conversations_owner_all on public.ai_conversations for all using (student_id = auth.uid()) with check (student_id = auth.uid());
drop policy if exists messages_owner_all on public.ai_messages;
create policy messages_owner_all on public.ai_messages for all
using (exists (select 1 from public.ai_conversations c where c.id = conversation_id and c.student_id = auth.uid()))
with check (exists (select 1 from public.ai_conversations c where c.id = conversation_id and c.student_id = auth.uid()));

drop policy if exists quizzes_visible_to_creator_or_student on public.quizzes;
create policy quizzes_visible_to_creator_or_student on public.quizzes for select
using (creator_id = auth.uid() or (is_published = true and stage = coalesce((select p.stage from public.profiles p where p.id = auth.uid()), stage)));
drop policy if exists quizzes_teacher_manage on public.quizzes;
create policy quizzes_teacher_manage on public.quizzes for all
using (creator_id = auth.uid() and exists (select 1 from public.profiles p where p.id = auth.uid() and p.role in ('teacher','admin')))
with check (creator_id = auth.uid() and exists (select 1 from public.profiles p where p.id = auth.uid() and p.role in ('teacher','admin')));

drop policy if exists quiz_questions_read on public.quiz_questions;
create policy quiz_questions_read on public.quiz_questions for select
using (exists (select 1 from public.quizzes q where q.id = quiz_id and (q.creator_id = auth.uid() or q.is_published = true)));
drop policy if exists quiz_questions_teacher_manage on public.quiz_questions;
create policy quiz_questions_teacher_manage on public.quiz_questions for all
using (exists (select 1 from public.quizzes q join public.profiles p on p.id = auth.uid() where q.id = quiz_id and q.creator_id = auth.uid() and p.role in ('teacher','admin')))
with check (exists (select 1 from public.quizzes q join public.profiles p on p.id = auth.uid() where q.id = quiz_id and q.creator_id = auth.uid() and p.role in ('teacher','admin')));

drop policy if exists assignments_student_or_teacher_read on public.quiz_assignments;
create policy assignments_student_or_teacher_read on public.quiz_assignments for select
using (student_id = auth.uid() or assigned_by = auth.uid());
drop policy if exists assignments_teacher_manage on public.quiz_assignments;
create policy assignments_teacher_manage on public.quiz_assignments for all
using (assigned_by = auth.uid()) with check (assigned_by = auth.uid());

drop policy if exists attempts_student_or_quiz_creator_read on public.quiz_attempts;
create policy attempts_student_or_quiz_creator_read on public.quiz_attempts for select
using (student_id = auth.uid() or exists (select 1 from public.quizzes q where q.id = quiz_id and q.creator_id = auth.uid()));
drop policy if exists attempts_student_insert on public.quiz_attempts;
create policy attempts_student_insert on public.quiz_attempts for insert with check (student_id = auth.uid());
drop policy if exists attempts_student_update_pending on public.quiz_attempts;
create policy attempts_student_update_pending on public.quiz_attempts for update
using (student_id = auth.uid() and submitted_at is null) with check (student_id = auth.uid());

drop policy if exists answers_student_or_teacher_read on public.quiz_answers;
create policy answers_student_or_teacher_read on public.quiz_answers for select
using (exists (select 1 from public.quiz_attempts a left join public.quizzes q on q.id = a.quiz_id where a.id = attempt_id and (a.student_id = auth.uid() or q.creator_id = auth.uid())));
drop policy if exists answers_student_write_before_submit on public.quiz_answers;
create policy answers_student_write_before_submit on public.quiz_answers for insert
with check (exists (select 1 from public.quiz_attempts a where a.id = attempt_id and a.student_id = auth.uid() and a.submitted_at is null));
drop policy if exists answers_student_update_before_submit on public.quiz_answers;
create policy answers_student_update_before_submit on public.quiz_answers for update
using (exists (select 1 from public.quiz_attempts a where a.id = attempt_id and a.student_id = auth.uid() and a.submitted_at is null))
with check (exists (select 1 from public.quiz_attempts a where a.id = attempt_id and a.student_id = auth.uid() and a.submitted_at is null));

drop policy if exists groups_teacher_manage on public.teacher_groups;
create policy groups_teacher_manage on public.teacher_groups for all
using (teacher_id = auth.uid()) with check (teacher_id = auth.uid());
drop policy if exists group_members_visible on public.group_members;
create policy group_members_visible on public.group_members for select
using (student_id = auth.uid() or exists (select 1 from public.teacher_groups g where g.id = group_id and g.teacher_id = auth.uid()));
drop policy if exists group_members_teacher_manage on public.group_members;
create policy group_members_teacher_manage on public.group_members for all
using (exists (select 1 from public.teacher_groups g where g.id = group_id and g.teacher_id = auth.uid()))
with check (exists (select 1 from public.teacher_groups g where g.id = group_id and g.teacher_id = auth.uid()));

drop policy if exists mastery_owner_all on public.student_mastery;
create policy mastery_owner_all on public.student_mastery for all using (student_id = auth.uid()) with check (student_id = auth.uid());
drop policy if exists notifications_owner_all on public.notifications;
create policy notifications_owner_all on public.notifications for all using (user_id = auth.uid()) with check (user_id = auth.uid());

-- Important: keep quiz answer keys inaccessible to students in production.
-- Move answer_key to a private table or expose questions through a server route that strips it.
-- Never put Supabase service-role keys or AI provider secrets in NEXT_PUBLIC_* variables.
