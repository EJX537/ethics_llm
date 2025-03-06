import { createClient } from "@libsql/client/web";

const dbUrl = import.meta.env.VITE_TURSO_DATABASE_URL as string;
const authToken = import.meta.env.VITE_TURSO_AUTH_TOKEN as string;


// Validate that we have the required values
if (!dbUrl) {
    console.error("Missing VITE_TURSO_DATABASE_URL environment variable");
}

const turso = createClient({
    url: dbUrl,
    authToken: authToken,
});

console.log("turso", turso);

export { turso };