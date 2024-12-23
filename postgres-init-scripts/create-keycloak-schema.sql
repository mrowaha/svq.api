-- Create the keycloak_schema if it does not exist
DO $$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM information_schema.schemata WHERE schema_name = 'keycloak_schema') THEN
      CREATE SCHEMA keycloak_schema;
   END IF;
END $$;