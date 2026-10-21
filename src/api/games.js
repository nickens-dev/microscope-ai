export async function createGame(input) {
  const response = await fetch("/api/games", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(input),
  });

  const responseBody = await response.json();

  if (!response.ok) {
    throw new Error(getErrorMessage(responseBody));
  }

  return responseBody;
}

function getErrorMessage(responseBody) {
  if (typeof responseBody?.detail === "string") {
    return responseBody.detail;
  }

  if (Array.isArray(responseBody?.detail)) {
    return responseBody.detail
      .map((error) => error.msg)
      .join(" ");
  }

  return "The game could not be created.";
}