export async function request(data) {
  const config = {
    mode: "no-cors",
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
    redirect: "follow",
  };

  try {
    const response = await fetch(
      "https://oc2efhjwph.execute-api.eu-central-1.amazonaws.com/prod/v1",
      config
    );
    return response;
  } catch (error) {
    console.log(error);
    return {
      ok: false,
      error: error,
    };
  }
}
