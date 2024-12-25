function getCSRFToken() {
    const regex = /csrftoken=([a-zA-Z0-9]*)/gm;
    const result = regex.exec(document.cookie);
    if (result.length > 0) {
        return result[1];
    } else {
        return null;
    }
}

function onLikeButtonClick(event) {
    const token = getCSRFToken();
    if (token) {
        const type = event.target.dataset.questionId;
        const id = event.target.dataset.questionId ?? event.target.dataset.answerId;

        const form = new FormData();
        form.append("type", type ? 0 : 1);
        form.append("id", id);
        form.append("csrfmiddlewaretoken", token);

        fetch("/make_like", {
            method: "POST",
            body: form,
        }).then(async (response) => {
            if (response.status == 200) {
                const data = await response.json();
                if (!data.error) {
                    const likes = document.getElementById(`${type ? "question" : "answer"}_${id}_likes`);
                    likes.innerText = data.likes_count;

                    event.target.src = event.target.src.includes("no_like")
                        ? event.target.src.replace("no_like", "like")
                        : event.target.src.replace("like", "no_like");
                }
            }
        }).catch(console.log);

    } else {
        window.location.replace("/login?continue=" + window.location.pathname);
    }
}

function onRightAnswerClick(event) {
    const token = getCSRFToken();
    if (token) {
        const question = event.target.dataset.questionId;
        const answer = event.target.dataset.answerId;

        const form = new FormData();
        form.append("question", question);
        form.append("answer", answer);
        form.append("csrfmiddlewaretoken", token);

        fetch("/question/right", {
            method: "POST",
            body: form,
        }).then(async (response) => {
            if (response.status == 200) {
                const data = await response.json();
                if (data.error) {
                    console.log("Error code:", data);
                }
            }
        }).catch(console.log);

    } else {
        window.location.replace("/login?continue=" + window.location.pathname);
    }
}