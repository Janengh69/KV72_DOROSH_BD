#  КВ-72 Дорош Карина
##  Лабораторна робота №2
### Ознайомлення з базовими операціями СУБД PostgreSQL
#### Варіант №4
**[Посилання](https://docs.google.com/document/d/1HRYdYICEkETOSFuok1jywzDriqnLt-tQhTs8fu8qGAs/edit?usp=sharing) на документ з описом структури БД**  
   
   **Сутності**
1) **Клієнт:**
  - Тип клієнту;
  - ПІБ;
  - Номер телефону;
  - Адреса.
  ```
CREATE TABLE public.client
(
    full_name text COLLATE pg_catalog."default" NOT NULL,
    client_type text COLLATE pg_catalog."default" NOT NULL,
    client_number text COLLATE pg_catalog."default" NOT NULL,
    adress integer,
    CONSTRAINT client_pkey PRIMARY KEY (client_number),
    CONSTRAINT chk_client_type CHECK (client_type = ANY (ARRAY['recipient'::text, 'sender'::text]))
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.client
    OWNER to postgres;
    
 ```

2) **Працівник:**
  - ID;
  - ПІБ;
  - Посада;
  - Години роботи;
  - Заробітня плата.
  ```
CREATE TABLE public.worker
(
    id integer NOT NULL DEFAULT nextval('"Worker_ID_seq"'::regclass),
    full_name text COLLATE pg_catalog."default" NOT NULL,
    "position" text COLLATE pg_catalog."default" NOT NULL,
    working_hours text COLLATE pg_catalog."default",
    salary integer NOT NULL,
    dep_number integer,
    CONSTRAINT "Worker_pkey" PRIMARY KEY (id),
    CONSTRAINT dep_number FOREIGN KEY (dep_number
        REFERENCES public.department (number_d) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT check_position CHECK ("position" = ANY (ARRAY['heavier'::text, 'casher'::text, 'manager'::text]))
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.worker
    OWNER to postgres;
```
3) **Вантаж:**
  - Штрихкод;
  - Тип вантажу;
  - Оголошена вартість.
  ``` 
CREATE TABLE public.cargo
(
    barcode text COLLATE pg_catalog."default" NOT NULL,
    cargo_type text COLLATE pg_catalog."default" NOT NULL,
    estimated_value numeric(10,2),
    client_id text COLLATE pg_catalog."default" NOT NULL,
    worker_id integer NOT NULL,
    delivered boolean,
    CONSTRAINT cargo_pkey PRIMARY KEY (barcode),
    CONSTRAINT client_id_ref FOREIGN KEY (client_id)
        REFERENCES public.client (client_number) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT check_barcode CHECK (length(barcode) < 10)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.cargo
    OWNER to postgres;

COMMENT ON COLUMN public.cargo.delivered
    IS 'comment';

-- Index: fki_client_id_ref

-- DROP INDEX public.fki_client_id_ref;

CREATE INDEX fki_client_id_ref
    ON public.cargo USING btree
    (client_id COLLATE pg_catalog."default")
    TABLESPACE pg_default;
 ```
4) **Пакування:**
  - Код пакування;
  - Тип пакування;
  - Кількість;
  - Ціна;
  - Вага.
```
CREATE TABLE public.packing
(
    packing_code integer NOT NULL,
    packing_type text COLLATE pg_catalog."default" NOT NULL,
    amount integer NOT NULL,
    price numeric(4,2) NOT NULL,
    weight numeric(6,2) NOT NULL,
    cargo_barcode text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT packing_pkey PRIMARY KEY (packing_code),
    CONSTRAINT packing_cargo FOREIGN KEY (cargo_barcode)
        REFERENCES public.cargo (barcode) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT weight_check CHECK (weight < 1000::numeric) NOT VALID,
    CONSTRAINT check_weight CHECK (weight < 1000::numeric)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.packing
    OWNER to postgres;
  ```
  
5) **Відділення:**
  - Номер відділення;
  - Адреса;
  - Тип відділення.
  ```
  CREATE TABLE public.department
(
    number_d integer NOT NULL,
    adress text COLLATE pg_catalog."default" NOT NULL,
    d_type text COLLATE pg_catalog."default" NOT NULL,
    street_number text COLLATE pg_catalog."default",
    CONSTRAINT department_pkey PRIMARY KEY (number_d),
    CONSTRAINT check_dep CHECK (number_d < 400),
    CONSTRAINT chk_dep_type CHECK (d_type = ANY (ARRAY['cargo'::text, 'postal'::text, 'mini'::text]))
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.department
    OWNER to postgres;
  ```


