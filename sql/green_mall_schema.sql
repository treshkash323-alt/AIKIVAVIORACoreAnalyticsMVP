-- =========================================
-- AIKIVAVIORA GreenMall Lab
-- Core Analytics Schema v0.1
-- =========================================

create table if not exists ai_dialogs (

    id bigint generated always as identity primary key,

    created_at timestamp with time zone default timezone('utc', now()),

    session_id text not null,

    user_role text,

    user_message text not null,

    ai_response text,

    ai_agent text,

    sentiment text,

    stage text,

    validation_status text,

    notes text

);