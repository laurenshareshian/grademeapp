--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3 (Ubuntu 12.3-1.pgdg16.04+1)
-- Dumped by pg_dump version 12.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: assignment; Type: TABLE; Schema: public; Owner: dnksgzdceixveu
--

CREATE TABLE public.assignment (
    assignment_id integer NOT NULL,
    title character varying(50) NOT NULL,
    description character varying(200) NOT NULL,
    due date NOT NULL,
    points integer NOT NULL,
    course integer
);


ALTER TABLE public.assignment OWNER TO dnksgzdceixveu;

--
-- Name: assignment_assignment_id_seq; Type: SEQUENCE; Schema: public; Owner: dnksgzdceixveu
--

CREATE SEQUENCE public.assignment_assignment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.assignment_assignment_id_seq OWNER TO dnksgzdceixveu;

--
-- Name: assignment_assignment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dnksgzdceixveu
--

ALTER SEQUENCE public.assignment_assignment_id_seq OWNED BY public.assignment.assignment_id;


--
-- Name: course; Type: TABLE; Schema: public; Owner: dnksgzdceixveu
--

CREATE TABLE public.course (
    course_id integer NOT NULL,
    title character varying(50) NOT NULL,
    section integer NOT NULL,
    department character varying(50) NOT NULL,
    description character varying(200) NOT NULL,
    units real NOT NULL,
    teacher integer
);


ALTER TABLE public.course OWNER TO dnksgzdceixveu;

--
-- Name: course_course_id_seq; Type: SEQUENCE; Schema: public; Owner: dnksgzdceixveu
--

CREATE SEQUENCE public.course_course_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.course_course_id_seq OWNER TO dnksgzdceixveu;

--
-- Name: course_course_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dnksgzdceixveu
--

ALTER SEQUENCE public.course_course_id_seq OWNED BY public.course.course_id;


--
-- Name: student; Type: TABLE; Schema: public; Owner: dnksgzdceixveu
--

CREATE TABLE public.student (
    student_id integer NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    year integer NOT NULL,
    email character varying(50) NOT NULL,
    telephone character varying(10)
);


ALTER TABLE public.student OWNER TO dnksgzdceixveu;

--
-- Name: student_course; Type: TABLE; Schema: public; Owner: dnksgzdceixveu
--

CREATE TABLE public.student_course (
    course_id integer NOT NULL,
    student_id integer NOT NULL
);


ALTER TABLE public.student_course OWNER TO dnksgzdceixveu;

--
-- Name: student_student_id_seq; Type: SEQUENCE; Schema: public; Owner: dnksgzdceixveu
--

CREATE SEQUENCE public.student_student_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.student_student_id_seq OWNER TO dnksgzdceixveu;

--
-- Name: student_student_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dnksgzdceixveu
--

ALTER SEQUENCE public.student_student_id_seq OWNED BY public.student.student_id;


--
-- Name: student_submission; Type: TABLE; Schema: public; Owner: dnksgzdceixveu
--

CREATE TABLE public.student_submission (
    student_id integer NOT NULL,
    submission_id integer NOT NULL
);


ALTER TABLE public.student_submission OWNER TO dnksgzdceixveu;

--
-- Name: submission; Type: TABLE; Schema: public; Owner: dnksgzdceixveu
--

CREATE TABLE public.submission (
    submission_id integer NOT NULL,
    submitted timestamp without time zone,
    grade integer,
    assignment integer,
    CONSTRAINT valid_grade CHECK ((0 <= grade))
);


ALTER TABLE public.submission OWNER TO dnksgzdceixveu;

--
-- Name: submission_submission_id_seq; Type: SEQUENCE; Schema: public; Owner: dnksgzdceixveu
--

CREATE SEQUENCE public.submission_submission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.submission_submission_id_seq OWNER TO dnksgzdceixveu;

--
-- Name: submission_submission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dnksgzdceixveu
--

ALTER SEQUENCE public.submission_submission_id_seq OWNED BY public.submission.submission_id;


--
-- Name: teacher; Type: TABLE; Schema: public; Owner: dnksgzdceixveu
--

CREATE TABLE public.teacher (
    teacher_id integer NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    email character varying(50) NOT NULL,
    telephone character varying(10)
);


ALTER TABLE public.teacher OWNER TO dnksgzdceixveu;

--
-- Name: teacher_teacher_id_seq; Type: SEQUENCE; Schema: public; Owner: dnksgzdceixveu
--

CREATE SEQUENCE public.teacher_teacher_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.teacher_teacher_id_seq OWNER TO dnksgzdceixveu;

--
-- Name: teacher_teacher_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dnksgzdceixveu
--

ALTER SEQUENCE public.teacher_teacher_id_seq OWNED BY public.teacher.teacher_id;


--
-- Name: assignment assignment_id; Type: DEFAULT; Schema: public; Owner: dnksgzdceixveu
--

ALTER TABLE ONLY public.assignment ALTER COLUMN assignment_id SET DEFAULT nextval('public.assignment_assignment_id_seq'::regclass);


--
-- Name: course course_id; Type: DEFAULT; Schema: public; Owner: dnksgzdceixveu
--

ALTER TABLE ONLY public.course ALTER COLUMN course_id SET DEFAULT nextval('public.course_course_id_seq'::regclass);


--
-- Name: student student_id; Type: DEFAULT; Schema: public; Owner: dnksgzdceixveu
--

ALTER TABLE ONLY public.student ALTER COLUMN student_id SET DEFAULT nextval('public.student_student_id_seq'::regclass);


--
-- Name: submission submission_id; Type: DEFAULT; Schema: public; Owner: dnksgzdceixveu
--

ALTER TABLE ONLY public.submission ALTER COLUMN submission_id SET DEFAULT nextval('public.submission_submission_id_seq'::regclass);


--
-- Name: teacher teacher_id; Type: DEFAULT; Schema: public; Owner: dnksgzdceixveu
--

ALTER TABLE ONLY public.teacher ALTER COLUMN teacher_id SET DEFAULT nextval('public.teacher_teacher_id_seq'::regclass);


--
-- Data for Name: assignment; Type: TABLE DATA; Schema: public; Owner: dnksgzdceixveu
--

COPY public.assignment (assignment_id, title, description, due, points, course) FROM stdin;
1	HW 1	Book exercises	2020-01-01	5	1
2	Group Project	Derivatives	2020-01-02	50	1
3	Exam 1	Slope	2020-01-02	50	3
4	Basket 1	basket	2020-01-02	100	2
5	Foot tickle	tickle	2020-01-02	100	4
6	HW Exercises	chapter 1	2020-01-02	100	6
7	Chewing	Vertical motion	2020-01-02	80	7
8	Rye	Color and odor	2020-01-02	100	8
9	Confuse a cat	Stun and alarm	2020-01-02	100	9
10	Basic steps	Swing those hoofs	2020-01-02	50	10
\.


--
-- Data for Name: course; Type: TABLE DATA; Schema: public; Owner: dnksgzdceixveu
--

COPY public.course (course_id, title, section, department, description, units, teacher) FROM stdin;
1	Calculus	100	Math	Integrals	4	1
2	Basketweaving	400	Art	Weaving stuff	3	2
3	Algebra	100	Math	Functions	3	1
4	Advanced Tickling	100	HR Problems	Creepy stuff	5	\N
5	Expensive Remote Learning Course	100	Science	same price as an in-person class without any labs	5	3
6	Electricity	100	Science	electricity stuff	5	4
7	Principles of Eating	101	Food	Chewing and swallowing	5	5
8	Analysis of Toast	505	Food	The rise and fall of hot bread in society	3	5
9	Milk	403	Food	Tolerating intolerance	5	5
10	Confusion	202	Philosophy	Utilizing uncertainty and stupidity	4	6
11	Trotting	103	Physical Education	Techniques and survey of graceful stomping	1	6
\.


--
-- Data for Name: student; Type: TABLE DATA; Schema: public; Owner: dnksgzdceixveu
--

COPY public.student (student_id, first_name, last_name, year, email, telephone) FROM stdin;
1	Kanye	West	2020	kanye@gmail.com	6094397996
2	Anthony	Fauci	2021	fauci@gmail.com	5555555555
3	Tiger	King	2021	iluvtigers@gmail.com	5555555555
4	Lion	King	2021	iluvlionss@gmail.com	5555555555
5	Charles	Lindberg	1922	wheresmykid@now.huh	5555555555
6	Amelia	Earhart	1931	mapsareforwimps@oce.an	5555555555
7	Howard	Hughes	1928	luvgoose@how.hu	5555555555
8	Bessie	Coleman	1905	suckitchumps@up.here	5555555555
9	Glenn	Curtiss	1911	needmoredanger@me.now	5555555555
\.


--
-- Data for Name: student_course; Type: TABLE DATA; Schema: public; Owner: dnksgzdceixveu
--

COPY public.student_course (course_id, student_id) FROM stdin;
1	1
2	1
3	1
1	2
1	3
3	2
5	3
7	5
10	6
8	7
9	8
9	9
\.


--
-- Data for Name: student_submission; Type: TABLE DATA; Schema: public; Owner: dnksgzdceixveu
--

COPY public.student_submission (student_id, submission_id) FROM stdin;
1	2
1	3
2	1
2	4
1	5
3	3
\.


--
-- Data for Name: submission; Type: TABLE DATA; Schema: public; Owner: dnksgzdceixveu
--

COPY public.submission (submission_id, submitted, grade, assignment) FROM stdin;
2	2020-06-09 12:14:11	72	1
3	2020-06-09 12:14:11	90	2
4	2020-06-09 12:14:11	60	3
1	2020-06-09 12:14:11	56	1
\.


--
-- Data for Name: teacher; Type: TABLE DATA; Schema: public; Owner: dnksgzdceixveu
--

COPY public.teacher (teacher_id, first_name, last_name, email, telephone) FROM stdin;
1	Lauren	Shareshian	lauren@gmail.com	6094397996
2	Joshua	Cox	cox@gmail.com	5555555555
3	Elon	Musk Baby	baby@gmail.com	5555555555
4	5G	Conspiracy Theorist	5G@gmail.com	5555555555
5	Dante	Aligheri	florencesux@gmail.com	5555555555
6	Sea	Biscuit	getoffmyback@gmail.com	5555555555
\.


--
-- Name: assignment_assignment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dnksgzdceixveu
--

SELECT pg_catalog.setval('public.assignment_assignment_id_seq', 10, true);


--
-- Name: course_course_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dnksgzdceixveu
--

SELECT pg_catalog.setval('public.course_course_id_seq', 11, true);


--
-- Name: student_student_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dnksgzdceixveu
--

SELECT pg_catalog.setval('public.student_student_id_seq', 9, true);


--
-- Name: submission_submission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dnksgzdceixveu
--

SELECT pg_catalog.setval('public.submission_submission_id_seq', 4, true);


--
-- Name: teacher_teacher_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dnksgzdceixveu
--

SELECT pg_catalog.setval('public.teacher_teacher_id_seq', 6, true);


--
-- Name: assignment assignment_pkey; Type: CONSTRAINT; Schema: public; Owner: dnksgzdceixveu
--

ALTER TABLE ONLY public.assignment
    ADD CONSTRAINT assignment_pkey PRIMARY KEY (assignment_id);


--
-- Name: course course_pkey; Type: CONSTRAINT; Schema: public; Owner: dnksgzdceixveu
--

ALTER TABLE ONLY public.course
    ADD CONSTRAINT course_pkey PRIMARY KEY (course_id);


--
-- Name: student_course student_course_pkey; Type: CONSTRAINT; Schema: public; Owner: dnksgzdceixveu
--

ALTER TABLE ONLY public.student_course
    ADD CONSTRAINT student_course_pkey PRIMARY KEY (course_id, student_id);


--
-- Name: student student_pkey; Type: CONSTRAINT; Schema: public; Owner: dnksgzdceixveu
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_pkey PRIMARY KEY (student_id);


--
-- Name: student_submission student_submission_pkey; Type: CONSTRAINT; Schema: public; Owner: dnksgzdceixveu
--

ALTER TABLE ONLY public.student_submission
    ADD CONSTRAINT student_submission_pkey PRIMARY KEY (student_id, submission_id);


--
-- Name: submission submission_pkey; Type: CONSTRAINT; Schema: public; Owner: dnksgzdceixveu
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_pkey PRIMARY KEY (submission_id);


--
-- Name: teacher teacher_pkey; Type: CONSTRAINT; Schema: public; Owner: dnksgzdceixveu
--

ALTER TABLE ONLY public.teacher
    ADD CONSTRAINT teacher_pkey PRIMARY KEY (teacher_id);


--
-- Name: LANGUAGE plpgsql; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON LANGUAGE plpgsql TO dnksgzdceixveu;


--
-- PostgreSQL database dump complete
--

