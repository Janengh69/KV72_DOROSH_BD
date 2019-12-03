create index on cargo(barcode);
analyze;  //Query returned successfully in 324 msec.
explain (costs off) select * from cargo where barcode=831; -- 65msec Index Scan using cargo_worker_id_idx on cargo

explain (costs off) select * from cargo where worker_id>831;                                -- Seq Scan on cargo (actual time=0.009..1.353 rows=5000 loops=1)
                                                                                            -- Filter: (worker_id > 831)
                                                                                            -- Planning Time: 0.122 ms
                                                                                            -- Execution Time: 1.716 ms


create index on cargo(estimated_value); 196msec
explain (analyze, costs off) select barcode from cargo where worker_id>(select avg(worker_id) from cargo) and estimated_value = 600;
                                                                                        -- Bitmap Heap Scan on cargo (actual time=0.478..0.478 rows=0 loops=1)
                                                                                        -- Recheck Cond: (estimated_value = '600'::numeric)
                                                                                        -- Filter: ((worker_id)::numeric > $0)
                                                                                        -- - Execution Time: 0.037 ms
                                                                                        -- Heap Blocks: exact=1
                                                                                        -- InitPlan 1 (returns $0)
                                                                                        -- ->  Aggregate (actual time=0.448..0.449 rows=1 loops=1)
                                                                                        -- ->  Seq Scan on cargo cargo_1 (actual time=0.011..0.192 rows=1340 loops=1)
                                                                                        -- ->  Bitmap Index Scan on cargo_estimated_value_idx (actual time=0.018..0.019 rows=1 loops=1)
                                                                                        -- Index Cond: (estimated_value = '600'::numeric)
                                                                                        -- Planning Time: 0.497 ms
                                                                                        -- Execution Time: 0.521 ms
--                                                                                             covering index
vacuum cargo;
select avg(worker_id) from cargo;
explain (analyze, costs off) select barcode from cargo where worker_id>6283;
                                                                                            --   Index Scan using cargo_worker_id_idx on cargo (actual time=0.019..0.787 rows=2500 loops=1)
                                                                                            --   Index Cond: (worker_id > 6283)
                                                                                            --   Planning Time: 0.083 ms
                                                                                           --   Execution Time: 0.920 ms
explain (costs off) select barcode from cargo where worker_id> (select avg(worker_id) from cargo);
                                                                                            -- Seq Scan on cargo (actual time=1.139..1.414 rows=670 loops=1)
                                                                                            -- Filter: ((worker_id)::numeric > $0)
                                                                                            -- Rows Removed by Filter: 670
                                                                                            -- InitPlan 1 (returns $0)
                                                                                            -- ->  Aggregate (actual time=0.613..0.614 rows=1 loops=1)
                                                                                            -- ->  Seq Scan on cargo cargo_1 (actual time=0.006..0.360 rows=1340 loops=1)
                                                                                            -- Planning Time: 0.172 ms
                                                                                            -- Execution Time: 1.494 ms
explain (analyze, costs off) select barcode from cargo where worker_id = (select MAX(worker_id) from cargo) and estimated_value = 600;
                                                                                            -- Index Scan using cargo_worker_id_idx on cargo (actual time=0.181..0.182 rows=0 loops=1)
                                                                                            -- Index Cond: (worker_id = $1)
                                                                                            -- Filter: (estimated_value = '600'::numeric)
                                                                                            -- Rows Removed by Filter: 1
                                                                                            -- InitPlan 2 (returns $1)
                                                                                            -- ->  Result (actual time=0.142..0.142 rows=1 loops=1)
                                                                                            -- InitPlan 1 (returns $0)
                                                                                            -- ->  Limit (actual time=0.134..0.136 rows=1 loops=1)
                                                                                            -- ->  Index Only Scan Backward using cargo_worker_id_idx on cargo cargo_1 (actual time=0.132..0.132 rows=1 loops=1)
                                                                                            -- Index Cond: (worker_id IS NOT NULL)
                                                                                            -- Heap Fetches: 0
                                                                                            -- Planning Time: 1.046 ms
                                                                                            -- Execution Time: 0.264 ms


create index on packing (packing_code, amount);
explain (analyze, costs off) select packing_code from packing where packing_code=(SELECT MIN(packing_code) from packing) and amount>(select avg(amount) from packing);
                                                                                        --     "Index Only Scan using packing_packing_code_amount_idx on packing (actual time=0.569..0.570 rows=0 loops=1)"
                                                                                        --     "  Index Cond: (packing_code = $1)"
                                                                                        --     "  Filter: ((amount)::numeric > $2)"
                                                                                        --     "  Rows Removed by Filter: 1"
                                                                                        --     "  Heap Fetches: 0"
                                                                                        --     "  InitPlan 2 (returns $1)"
                                                                                        --     "    ->  Result (actual time=0.050..0.050 rows=1 loops=1)"
                                                                                        --     "          InitPlan 1 (returns $0)"
                                                                                        --     "            ->  Limit (actual time=0.046..0.046 rows=1 loops=1)"
                                                                                        --     "                  ->  Index Only Scan using packing_packing_code_amount_idx on packing packing_1 (actual time=0.045..0.045 rows=1 loops=1)"
                                                                                        --     "                        Index Cond: (packing_code IS NOT NULL)"
                                                                                        --     "                        Heap Fetches: 0"
                                                                                        --     "  InitPlan 3 (returns $2)"
                                                                                        --     "    ->  Aggregate (actual time=0.487..0.488 rows=1 loops=1)"
                                                                                        --     "          ->  Seq Scan on packing packing_2 (actual time=0.014..0.327 rows=1340 loops=1)"
                                                                                        --     "Planning Time: 0.226 ms"
                                                                                        --     "Execution Time: 0.631 ms"
explain (analyze, costs off) select packing_code from packing where packing_code>831 and weight>10;




explain (analyze, costs off) select full_name from client where lower(full_name)='anyrak'
                                                                                        -- Seq Scan on client (actual time=5.132..5.132 rows=0 loops=1)
                                                                                        --   Filter: (lower(full_name) = 'anyrak'::text)
                                                                                        --   Rows Removed by Filter: 5000
                                                                                        --   Planning Time: 2.179 ms
                                                                                        --   Execution Time: 5.552 ms
create index on client(lower(full_name));
explain (analyze, costs off) select full_name from client where lower(full_name)='anyrak'
                                                                                        -- Bitmap Heap Scan on client (actual time=0.023..0.023 rows=0 loops=1)
                                                                                        -- Recheck Cond: (lower(full_name) = 'anyrak'::text)
                                                                                        -- ->  Bitmap Index Scan on client_lower_idx (actual time=0.021..0.021 rows=0 loops=1)
                                                                                        -- Index Cond: (lower(full_name) = 'anyrak'::text)
                                                                                        -- Planning Time: 0.159 ms
                                                                                        -- Execution Time: 0.045 ms


-- select a.amname, p.name, pg_indexam_has_property(a.oid,p.name)
-- from pg_am a,
-- unnest(array['can_order','can_unique','can_multi_col','can_exclude']) p(name)
-- where a.amname = 'brin' order by a.amname;

-- properties of brin indexes


create table ts(doc text, doc_tsv tsvector);
insert into ts(doc) values
  ('Во поле береза стояла'),  ('Во поле кудрявая стояла'),
  ('Люли, люли, стояла'),     ('Люли, люли, стояла'),
  ('Некому березу заломати'), ('Некому кудряву заломати'),
  ('Люли, люли, заломати'),   ('Люли, люли, заломати'),
  ('Я пойду погуляю'),        ('Белую березу заломаю'),
  ('Люли, люли, заломаю'),    ('Люли, люли, заломаю');
set default_text_search_config = russian;
update ts set doc_tsv = to_tsvector(doc);

create index on ts using gin(doc_tsv);
select ctid, doc, doc_tsv from ts;-- number of page and position on the page
select (unnest(doc_tsv)).lexeme, count(*) from ts group by 1 order by 2 desc;  -- amount of each words in document


explain(analyze, costs off)
select doc from ts where doc_tsv @@ to_tsquery('стояла & кудрявая');
--                                                                     Bitmap Heap Scan on ts (actual time=0.043..0.043 rows=1 loops=1)
--                                                                     Recheck Cond: (doc_tsv @@ to_tsquery('стояла & кудрявая'::text))
--                                                                     Heap Blocks: exact=1
--                                                                     ->  Bitmap Index Scan on ts_doc_tsv_idx (actual time=0.033..0.033 rows=1 loops=1)
--                                                                     Index Cond: (doc_tsv @@ to_tsquery('стояла & кудрявая'::text))
--                                                                     Planning Time: 0.233 ms
--                                                                     Execution Time: 0.077 ms



select doc from ts where doc_tsv @@ to_tsquery('залом:*');
                                                                    -- "Bitmap Heap Scan on ts  (cost=12.31..23.45 rows=7 width=37) (actual time=0.081..0.150 rows=189 loops=1)"
                                                                    -- "  Recheck Cond: (doc_tsv @@ to_tsquery('залом:*'::text))"
                                                                    -- "  Heap Blocks: exact=7"
                                                                    -- "  ->  Bitmap Index Scan on ts_doc_tsv_idx  (cost=0.00..12.31 rows=7 width=0) (actual time=0.072..0.072 rows=189 loops=1)"
                                                                    -- "        Index Cond: (doc_tsv @@ to_tsquery('залом:*'::text))"
                                                                    -- "Planning Time: 0.123 ms"
                                                                    -- "Execution Time: 0.194 ms"
select attname, correlation from pg_stats where tablename='cargo' order by correlation desc nulls last;

-- trigger after delete
CREATE OR REPLACE FUNCTION func() RETURNS trigger AS
$$BEGIN
IF OLD.price > 10 THEN
   UPDATE "cargo" SET estimated_value = estimated_value - 10
      WHERE barcode = OLD.cargo_barcode;
      END IF;
   RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER add_money
   AFTER DELETE ON packing FOR EACH ROW
   EXECUTE PROCEDURE func();
delete from packing where cargo_barcode = '26591'

select * from cargo where barcode = '179';
DELETE FROM packing where cargo_barcode = '179';
select * from packing where cargo_barcode = '179';

-- trigger after insert

CREATE OR REPLACE FUNCTION UPD()
RETURNS trigger AS
$$
begin
if new.salary > 10000 THEN
if new.full_name IS NULL THEN raise warning 'null full name %', now();
end if;
UPDATE worker SET full_name = (SELECT REVERSE (n2.full_name) from worker as n2 where (n2.id = worker.id));
END IF;
return new;
end;
$$ language plpgsql;

CREATE TRIGGER change_name
   AFTER INSERT ON worker FOR EACH ROW
   EXECUTE PROCEDURE UPD();

insert into worker (id, full_name, position, working_hours, salary, dep_number ) values (1, 'Karyna', 'manager', '17-21', 15000, 10)
insert into worker (id, position, working_hours, salary, dep_number ) values (2, 'manager', '17-21', 17000, 10)

select * from worker where id = 1;


-- transactions

-- 1)
START TRANSACTION ISOLATION LEVEL SERIALIZABLE;
select current_setting('transaction_isolation');


--2)
START TRANSACTION ISOLATION LEVEL REPEATABLE READ;
select current_setting('transaction_isolation');


3)
START TRANSACTION ISOLATION LEVEL READ COMMITTED;
select current_setting('transaction_isolation');
-- read commited

insert into client (full_name, client_number, client_type) values ('anyrak', '09658995', 'sender')
START TRANSACTION ISOLATION LEVEL READ COMMITTED;
select current_setting('transaction_isolation');
select * from department where number_d = 69
COMMIT
insert into department(number_d, address, d_type, street_number) values (69, 'Kovalskogo', 'postal', '8i')
delete from department where number_d=69
update department set street_number = '100'
rollback


select current_setting('transaction_isolation');
START TRANSACTION ISOLATION LEVEL READ COMMITTED;
select * from department;
commit
rollbACK



insert into department(number_d, address, d_type, street_number) values (69, 'Kovalskogo', 'postal', '8i')

select * from department where number_d = 69
update department set street_number = '10'


START TRANSACTION ISOLATION LEVEL REPEATABLE READ;
select current_setting('transaction_isolation');
select * from department where number_d = 69
COMMIT
rollback
delete from department where number_d=69
update department set street_number = '9'
START TRANSACTION ISOLATION LEVEL READ COMMITTED;






--- brin

CREATE INDEX idx_temperature_log_log_timestamp ON temperature_log USING BRIN (log_timestamp) WITH (pages_per_range = 128);

vacuum analyse;

EXPLAIN ANALYZE SELECT AVG(temperature) FROM temperature_log WHERE log_timestamp>='2016-04-04' AND log_timestamp<'2016-04-05';




CREATE TABLE temperature_log (log_id serial, sensor_id int, log_timestamp timestamp without time zone, temperature int);

INSERT INTO temperature_log(sensor_id,log_timestamp,temperature) VALUES (1,generate_series('2016-01-01'::timestamp,'2016-12-31'::timestamp,'1 second'),round(random()*100)::int);
                                                                        -- This will create 31536001 rows of sensor test data.
EXPLAIN ANALYZE SELECT AVG(temperature) FROM temperature_log WHERE log_timestamp>='2016-04-04' AND log_timestamp<'2016-04-05';
                                                                        --
                                                                            -- "Finalize Aggregate  (cost=415466.26..415466.27 rows=1 width=32) (actual time=19886.473..19886.473 rows=1 loops=1)"
                                                                            -- "  ->  Gather  (cost=415466.04..415466.25 rows=2 width=32) (actual time=19886.392..19898.631 rows=3 loops=1)"
                                                                            -- "        Workers Planned: 2"
                                                                            -- "        Workers Launched: 2"
                                                                            -- "        ->  Partial Aggregate  (cost=414466.04..414466.05 rows=1 width=32) (actual time=19864.624..19864.624 rows=1 loops=3)"
                                                                            -- "              ->  Parallel Seq Scan on temperature_log  (cost=0.00..414288.19 rows=71140 width=4) (actual time=5157.923..19850.356 rows=28800 loops=3)"
                                                                            -- "                    Filter: ((log_timestamp >= '2016-04-04 00:00:00'::timestamp without time zone) AND (log_timestamp < '2016-04-05 00:00:00'::timestamp without time zone))"
                                                                            -- "                    Rows Removed by Filter: 10483200"
                                                                            -- "Planning Time: 2.359 ms"
                                                                            -- "Execution Time: 19898.688 ms"

CREATE INDEX idx_temperature_log_log_timestamp ON temperature_log USING btree (log_timestamp);
 vacuum analyze;
  EXPLAIN ANALYZE SELECT AVG(temperature) FROM temperature_log WHERE log_timestamp>='2016-04-04' AND log_timestamp<'2016-04-05';
                                                                            -- "Aggregate  (cost=4169.11..4169.12 rows=1 width=32) (actual time=26.590..26.590 rows=1 loops=1)"
                                                                            -- "  ->  Index Scan using idx_temperature_log_log_timestamp on temperature_log  (cost=0.56..3907.82 rows=104513 width=4) (actual time=0.027..17.720 rows=86400 loops=1)"
                                                                            -- "        Index Cond: ((log_timestamp >= '2016-04-04 00:00:00'::timestamp without time zone) AND (log_timestamp < '2016-04-05 00:00:00'::timestamp without time zone))"
                                                                            -- "Planning Time: 0.082 ms"
                                                                            -- "Execution Time: 26.620 ms"

DROP INDEX idx_temperature_log_log_timestamp;


CREATE INDEX idx_temperature_log_log_timestamp ON temperature_log USING BRIN (log_timestamp) WITH (pages_per_range = 128);

vacuum analyse;

EXPLAIN ANALYZE SELECT AVG(temperature) FROM temperature_log WHERE log_timestamp>='2016-04-04' AND log_timestamp<'2016-04-05';

                                                                      --                                                                         "Finalize Aggregate  (cost=287057.40..287057.41 rows=1 width=32) (actual time=17.461..17.462 rows=1 loops=1)"
                                                                        -- "  ->  Gather  (cost=287057.18..287057.39 rows=2 width=32) (actual time=17.374..19.921 rows=3 loops=1)"
                                                                        -- "        Workers Planned: 2"
                                                                        -- "        Workers Launched: 2"
                                                                        -- "        ->  Partial Aggregate  (cost=286057.18..286057.19 rows=1 width=32) (actual time=13.063..13.064 rows=1 loops=3)"
                                                                        -- "              ->  Parallel Bitmap Heap Scan on temperature_log  (cost=54.39..285968.71 rows=35388 width=4) (actual time=0.584..9.113 rows=28800 loops=3)"
                                                                        -- "                    Recheck Cond: ((log_timestamp >= '2016-04-04 00:00:00'::timestamp without time zone) AND (log_timestamp < '2016-04-05 00:00:00'::timestamp without time zone))"
                                                                        -- "                    Rows Removed by Index Recheck: 4693"
                                                                        -- "                    Heap Blocks: lossy=263"
                                                                        -- "                    ->  Bitmap Index Scan on idx_temperature_log_log_timestamp  (cost=0.00..33.16 rows=100434 width=0) (actual time=1.128..1.129 rows=6400 loops=1)"
                                                                        -- "                          Index Cond: ((log_timestamp >= '2016-04-04 00:00:00'::timestamp without time zone) AND (log_timestamp < '2016-04-05 00:00:00'::timestamp without time zone))"
                                                                        -- "Planning Time: 0.122 ms"
                                                                        -- "Execution Time: 20.006 ms"