-- Create users table
CREATE TABLE public.users (
    id uuid NOT NULL,
    name character varying(64) NOT NULL,
    surname character varying(64) NOT NULL,
    patronymic character varying(64),
    password_hash character varying(255) NOT NULL,
    type character varying(16) NOT NULL,
    class_name character varying(8),
    login character varying(255) NOT NULL,
    subject character varying(64),
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT valid_user_type CHECK (type IN ('teacher', 'student', 'headteacher')),
    CONSTRAINT users_login_key UNIQUE (login)
); 
