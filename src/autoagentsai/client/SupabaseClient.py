from supabase import create_client


class SupabaseClient:
    def __init__(self, supabase_url: str, supabase_anon_key: str, supabase_service_key: str):
        self.supabase_url = supabase_url
        self.supabase_anon_key = supabase_anon_key
        self.supabase_service_key = supabase_service_key
        self.supabase_client = create_client(self.supabase_url, self.supabase_anon_key)

    def get_client(self):
        return self.supabase_client

    def create_table(self, table_name: str, columns: list[dict]):
        self.supabase_client.schema(table_name).create_table(columns)

        