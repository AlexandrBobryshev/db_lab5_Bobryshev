DO $$ -- процедура без імені
 DECLARE
     order_id   orders.order_number%TYPE;

 BEGIN
     order_id := 16200;
   
     FOR counter IN 1..10
         LOOP
            INSERT INTO orders (order_number, order_date)
             VALUES (counter + order_id, current_date - 10 + counter);
         END LOOP;
 END;
 $$;