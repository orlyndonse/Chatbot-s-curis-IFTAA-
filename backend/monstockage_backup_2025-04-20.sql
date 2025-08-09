--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: orly
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO orly;

--
-- Name: conversations; Type: TABLE; Schema: public; Owner: orly
--

CREATE TABLE public.conversations (
    uid uuid NOT NULL,
    title character varying NOT NULL,
    created_at timestamp without time zone NOT NULL,
    user_uid uuid NOT NULL
);


ALTER TABLE public.conversations OWNER TO orly;

--
-- Name: questions; Type: TABLE; Schema: public; Owner: orly
--

CREATE TABLE public.questions (
    uid uuid NOT NULL,
    title character varying NOT NULL,
    author character varying NOT NULL,
    publisher character varying NOT NULL,
    published_date date NOT NULL,
    page_count integer NOT NULL,
    language character varying NOT NULL,
    user_uid uuid,
    created_at timestamp without time zone NOT NULL,
    update_at timestamp without time zone NOT NULL,
    conversation_uid uuid
);


ALTER TABLE public.questions OWNER TO orly;

--
-- Name: questiontable3; Type: TABLE; Schema: public; Owner: orly
--

CREATE TABLE public.questiontable3 (
    question_id uuid NOT NULL,
    table3_id uuid NOT NULL
);


ALTER TABLE public.questiontable3 OWNER TO orly;

--
-- Name: reponses; Type: TABLE; Schema: public; Owner: orly
--

CREATE TABLE public.reponses (
    uid uuid NOT NULL,
    rating integer NOT NULL,
    reponse_text character varying NOT NULL,
    user_uid uuid,
    question_uid uuid,
    created_at timestamp without time zone NOT NULL,
    update_at timestamp without time zone NOT NULL
);


ALTER TABLE public.reponses OWNER TO orly;

--
-- Name: users; Type: TABLE; Schema: public; Owner: orly
--

CREATE TABLE public.users (
    uid uuid NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    role character varying DEFAULT 'user'::character varying NOT NULL,
    is_verified boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    update_at timestamp without time zone NOT NULL,
    verified_at timestamp without time zone,
    password_hash character varying NOT NULL
);


ALTER TABLE public.users OWNER TO orly;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: orly
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: conversations; Type: TABLE DATA; Schema: public; Owner: orly
--

COPY public.conversations (uid, title, created_at, user_uid) FROM stdin;
\.


--
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: orly
--

COPY public.questions (uid, title, author, publisher, published_date, page_count, language, user_uid, created_at, update_at, conversation_uid) FROM stdin;
6252dd13-1010-4af9-9fd2-4c131ee797d9	TEST DE CONVERSATION	user	frontend	2025-04-17	1	fr	9668d9c2-717e-4f83-9449-c80ce028f262	2025-04-17 07:06:57.760239	2025-04-17 07:06:57.760243	\N
7dc8ee9d-ce24-4020-a62d-95b895cc6dff	2ème test	Utilisateur	ChatBot	2025-04-17	1	fr	9668d9c2-717e-4f83-9449-c80ce028f262	2025-04-17 07:24:20.935609	2025-04-17 07:24:20.935613	\N
57db6969-26d7-4157-895c-5134c1f3f7df	3ème test	Utilisateur	ChatBot	2025-04-17	1	fr	9668d9c2-717e-4f83-9449-c80ce028f262	2025-04-17 07:24:54.578127	2025-04-17 07:24:54.57813	\N
6a1f4bd8-1a62-4909-885b-d803697ee42e	4ème test	Utilisateur	ChatBot	2025-04-17	1	fr	9668d9c2-717e-4f83-9449-c80ce028f262	2025-04-17 07:25:21.918975	2025-04-17 07:25:21.918978	\N
e74196aa-6505-4e6e-87f8-b5dc04414bcb	5ème test	Utilisateur	ChatBot	2025-04-17	1	fr	9668d9c2-717e-4f83-9449-c80ce028f262	2025-04-17 07:33:54.854706	2025-04-17 07:33:54.854711	\N
c646d857-35fe-4fb9-bfea-4c7931951531	6ème test	user	frontend	2025-04-17	1	fr	9668d9c2-717e-4f83-9449-c80ce028f262	2025-04-17 08:55:15.088169	2025-04-17 08:55:15.088215	\N
05ef673e-f3e6-40af-8e88-335368169155	hello	Utilisateur	ChatBot	2025-04-17	1	fr	ed48cc12-d055-4841-bcda-d38d54f50b71	2025-04-17 10:10:59.049338	2025-04-17 10:10:59.049343	\N
0f70f29d-2289-4056-b523-56dbcc5f3681	hello 22	Utilisateur	ChatBot	2025-04-17	1	fr	4473eab7-53b1-4f23-93f1-14d4df376f2e	2025-04-17 10:18:23.885764	2025-04-17 10:18:23.885769	\N
50e9526a-1665-4aa3-9feb-efbee1821c8a	yoo	Utilisateur	ChatBot	2025-04-17	1	fr	ed48cc12-d055-4841-bcda-d38d54f50b71	2025-04-17 10:36:14.934824	2025-04-17 10:36:14.934827	\N
bc77d66a-5abd-4cdd-969a-94d512304a22	next num 2	Utilisateur	ChatBot	2025-04-17	1	fr	4473eab7-53b1-4f23-93f1-14d4df376f2e	2025-04-17 22:15:42.456375	2025-04-17 22:15:42.456379	\N
0456718d-4559-4705-b91a-8df96f6b1001	gfjhgj	Utilisateur	ChatBot	2025-04-18	1	fr	4473eab7-53b1-4f23-93f1-14d4df376f2e	2025-04-18 14:57:47.446986	2025-04-18 14:57:47.446995	\N
9c3a2179-1e9a-4692-9b71-302ba3f749a1	thtrhezrher	Utilisateur	ChatBot	2025-04-18	1	fr	4473eab7-53b1-4f23-93f1-14d4df376f2e	2025-04-18 14:58:13.87791	2025-04-18 14:58:13.877914	\N
d14eff16-abdd-4855-88be-266e2dab5992	vjgh	Utilisateur	ChatBot	2025-04-19	1	fr	9668d9c2-717e-4f83-9449-c80ce028f262	2025-04-19 15:09:33.495992	2025-04-19 15:09:33.495997	\N
26bac292-9be1-4d0e-964c-a95f6bdf65ee	fdsf	Utilisateur	ChatBot	2025-04-19	1	fr	4473eab7-53b1-4f23-93f1-14d4df376f2e	2025-04-19 22:50:13.934549	2025-04-19 22:50:13.934553	\N
\.


--
-- Data for Name: questiontable3; Type: TABLE DATA; Schema: public; Owner: orly
--

COPY public.questiontable3 (question_id, table3_id) FROM stdin;
\.


--
-- Data for Name: reponses; Type: TABLE DATA; Schema: public; Owner: orly
--

COPY public.reponses (uid, rating, reponse_text, user_uid, question_uid, created_at, update_at) FROM stdin;
d00ab538-00d5-47f8-b352-08ddd960656b	4	Réponse générée automatiquement pour : TEST DE CONVERSATION	9668d9c2-717e-4f83-9449-c80ce028f262	6252dd13-1010-4af9-9fd2-4c131ee797d9	2025-04-17 07:06:57.779341	2025-04-17 07:06:57.779344
8b3a4dd6-3805-497a-95a7-a06895a42949	4	Réponse générée automatiquement pour : 2ème test	9668d9c2-717e-4f83-9449-c80ce028f262	7dc8ee9d-ce24-4020-a62d-95b895cc6dff	2025-04-17 07:24:20.955383	2025-04-17 07:24:20.955388
684a4792-ecd8-4f5e-9129-2a7ebd4dfb5b	4	Réponse générée automatiquement pour : 3ème test	9668d9c2-717e-4f83-9449-c80ce028f262	57db6969-26d7-4157-895c-5134c1f3f7df	2025-04-17 07:24:54.585933	2025-04-17 07:24:54.585937
e0e00544-8701-4ca7-87d7-61635afd5337	4	Réponse générée automatiquement pour : 4ème test	9668d9c2-717e-4f83-9449-c80ce028f262	6a1f4bd8-1a62-4909-885b-d803697ee42e	2025-04-17 07:25:21.926769	2025-04-17 07:25:21.926773
a86b94be-9245-4964-a329-64cd95c03662	4	Réponse générée automatiquement pour : 5ème test	9668d9c2-717e-4f83-9449-c80ce028f262	e74196aa-6505-4e6e-87f8-b5dc04414bcb	2025-04-17 07:33:54.87178	2025-04-17 07:33:54.871784
a0ab7b7f-5e65-45f7-81fe-3292fce83b46	4	Réponse générée automatiquement pour : hello 22	4473eab7-53b1-4f23-93f1-14d4df376f2e	0f70f29d-2289-4056-b523-56dbcc5f3681	2025-04-17 10:18:23.907043	2025-04-17 10:18:23.907047
1dd308ff-4832-4494-ad7c-8f288f521eae	4	Réponse générée automatiquement pour : yoo	ed48cc12-d055-4841-bcda-d38d54f50b71	50e9526a-1665-4aa3-9feb-efbee1821c8a	2025-04-17 10:36:14.942885	2025-04-17 10:36:14.94289
9f7346b1-0124-4bd4-b1f2-f6ccff1797d3	4	Réponse générée automatiquement pour : next num 2	4473eab7-53b1-4f23-93f1-14d4df376f2e	bc77d66a-5abd-4cdd-969a-94d512304a22	2025-04-17 22:15:42.476032	2025-04-17 22:15:42.476037
cc54694c-2ee2-45fb-9b39-b5697e3c969d	4	Réponse générée automatiquement pour : gfjhgj	4473eab7-53b1-4f23-93f1-14d4df376f2e	0456718d-4559-4705-b91a-8df96f6b1001	2025-04-18 14:57:47.474596	2025-04-18 14:57:47.474602
05186373-334e-465f-b379-4b7dcc1eed02	4	Réponse générée automatiquement pour : thtrhezrher	4473eab7-53b1-4f23-93f1-14d4df376f2e	9c3a2179-1e9a-4692-9b71-302ba3f749a1	2025-04-18 14:58:13.898681	2025-04-18 14:58:13.898687
b9d1542e-c167-4faa-9edd-bb65ada502f6	4	Réponse générée automatiquement pour : vjgh	9668d9c2-717e-4f83-9449-c80ce028f262	d14eff16-abdd-4855-88be-266e2dab5992	2025-04-19 15:09:33.515578	2025-04-19 15:09:33.515582
6478a251-65d7-4dab-b0a7-2126ed83ad6e	4	Réponse générée automatiquement pour : fdsf	4473eab7-53b1-4f23-93f1-14d4df376f2e	26bac292-9be1-4d0e-964c-a95f6bdf65ee	2025-04-19 22:50:13.955021	2025-04-19 22:50:13.955024
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: orly
--

COPY public.users (uid, username, email, first_name, last_name, role, is_verified, created_at, update_at, verified_at, password_hash) FROM stdin;
73e4cdd7-539a-446c-8901-25fc2f7f7fa9	user23	gabiamsamuelnathan@gmailcom	gabiam	samuel	user	f	2025-04-18 11:54:52.071963	2025-04-18 11:54:52.071968	\N	$2b$12$jgiaotW2hDf0T0g8sL0zteMb4oZ6B6A.67YLmwGF81fLnjQG/eFVa
2c2775a5-bbe6-441c-b4bf-f830a80056d0	user23	gabiamsamuelnathan@gmail.com	gabiam	samuel	user	f	2025-04-18 11:55:10.104639	2025-04-18 11:55:10.104644	\N	$2b$12$.EGwzjuBtBCnzfDlEHxSzuO1FE7xTM7pa/d.IMpudvYpxluE3uU6S
bb6164cf-104c-4051-8774-a383849b5722	orly	orlyndonrhffgh@gmail.com	user2Name	Orly	user	f	2025-04-18 19:11:18.641964	2025-04-18 19:11:18.641973	\N	$2b$12$A7LsqStkXpmhURfem0vVJe2DGeDXnpyCuD5r4v91wQE.KYnfOMUWi
9668d9c2-717e-4f83-9449-c80ce028f262	user2	orl.ndonse@gmail.com	user2	user2SecondName	user	t	2025-04-17 07:00:33.86665	2025-04-17 07:00:33.866656	2025-04-17 06:01:20.807057	$2b$12$ELW/FT5x3w97smMy7bo.VePha89nkI6iuRZQJPIL1wUoA8yQkH0fW
4473eab7-53b1-4f23-93f1-14d4df376f2e	orly	orlyndonse22@gmail.com	Ndonse	Orly	user	t	2025-04-17 05:46:41.123925	2025-04-17 05:46:41.123933	2025-04-17 04:47:07.3263	$2b$12$4aRs.kRtYG0mOhj5DyB94.6K2w4BUvc5Ysx0YSrPQTRc2Li/UO0zm
ed48cc12-d055-4841-bcda-d38d54f50b71	user	orlndosyl@gmail.com	user	userSecondName	user	t	2025-04-17 05:50:10.459403	2025-04-17 05:50:10.459408	2025-04-17 04:50:38.179762	$2b$12$hC6Nx78VAob3k9qKj6zf4uWg7.u5bBKDA8ofPwRk.YJlJQt/uJEi.
e6388550-9020-4d45-ad2d-600fb80c95ed	tony	etony@biu.bi	charmant	Egerimana	user	t	2025-04-19 15:55:11.341563	2025-04-19 15:55:11.341567	2025-04-19 14:56:24.979403	$2b$12$2hEdFkQLTqSkUsJZqHv91eFVJnMM2lPHVxEqjZIs1z79VdR2ckXDG
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: orly
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: conversations conversations_pkey; Type: CONSTRAINT; Schema: public; Owner: orly
--

ALTER TABLE ONLY public.conversations
    ADD CONSTRAINT conversations_pkey PRIMARY KEY (uid);


--
-- Name: questions questions_pkey; Type: CONSTRAINT; Schema: public; Owner: orly
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (uid);


--
-- Name: questiontable3 questiontable3_pkey; Type: CONSTRAINT; Schema: public; Owner: orly
--

ALTER TABLE ONLY public.questiontable3
    ADD CONSTRAINT questiontable3_pkey PRIMARY KEY (question_id, table3_id);


--
-- Name: reponses reponses_pkey; Type: CONSTRAINT; Schema: public; Owner: orly
--

ALTER TABLE ONLY public.reponses
    ADD CONSTRAINT reponses_pkey PRIMARY KEY (uid);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: orly
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (uid);


--
-- Name: conversations conversations_user_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: orly
--

ALTER TABLE ONLY public.conversations
    ADD CONSTRAINT conversations_user_uid_fkey FOREIGN KEY (user_uid) REFERENCES public.users(uid);


--
-- Name: questions questions_conversation_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: orly
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_conversation_uid_fkey FOREIGN KEY (conversation_uid) REFERENCES public.conversations(uid);


--
-- Name: questions questions_user_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: orly
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_user_uid_fkey FOREIGN KEY (user_uid) REFERENCES public.users(uid);


--
-- Name: questiontable3 questiontable3_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: orly
--

ALTER TABLE ONLY public.questiontable3
    ADD CONSTRAINT questiontable3_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(uid);


--
-- Name: reponses reponses_question_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: orly
--

ALTER TABLE ONLY public.reponses
    ADD CONSTRAINT reponses_question_uid_fkey FOREIGN KEY (question_uid) REFERENCES public.questions(uid);


--
-- Name: reponses reponses_user_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: orly
--

ALTER TABLE ONLY public.reponses
    ADD CONSTRAINT reponses_user_uid_fkey FOREIGN KEY (user_uid) REFERENCES public.users(uid);


--
-- PostgreSQL database dump complete
--

