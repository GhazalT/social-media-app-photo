function setBusy(form, isBusy) {
    const submitter = form.querySelector('button[type="submit"]');
    if (!submitter) {
        return;
    }

    if (!submitter.dataset.originalLabel) {
        submitter.dataset.originalLabel = submitter.textContent.trim();
    }

    submitter.disabled = isBusy;
    submitter.textContent = isBusy ? "Working..." : submitter.dataset.originalLabel;
}

const THEME_KEY = "photo-theme";

function getPreferredTheme() {
    try {
        const savedTheme = localStorage.getItem(THEME_KEY);
        if (savedTheme === "light" || savedTheme === "dark") {
            return savedTheme;
        }
    } catch (error) {
        return "light";
    }

    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
        ? "dark"
        : "light";
}

function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    document.body.dataset.theme = theme;
    document.querySelectorAll("[data-theme-label]").forEach((label) => {
        label.textContent = theme === "dark" ? "Light" : "Dark";
    });
    document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
        button.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
        button.title = theme === "dark" ? "Switch to light mode" : "Switch to dark mode";
    });
}

function setupThemeToggle() {
    applyTheme(getPreferredTheme());

    document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
        button.addEventListener("click", () => {
            const currentTheme = document.documentElement.dataset.theme === "dark" ? "dark" : "light";
            const nextTheme = currentTheme === "dark" ? "light" : "dark";

            try {
                localStorage.setItem(THEME_KEY, nextTheme);
            } catch (error) {
                // Theme should still change even when storage is unavailable.
            }

            applyTheme(nextTheme);
        });
    });
}

function setupFollowForms() {
    document.querySelectorAll("[data-follow-form]").forEach((form) => {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const button = form.querySelector("[data-follow-button]");
            const followersCount = document.querySelector("[data-followers-count]");
            const formData = new FormData(form);

            if (button) {
                button.disabled = true;
            }

            try {
                const response = await fetch(form.action, {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                    },
                });

                if (!response.ok) {
                    throw new Error("Follow request failed");
                }

                const data = await response.json();

                if (button) {
                    button.textContent = data.button_text;
                    button.classList.toggle("button-primary--muted", data.is_following);
                }

                if (followersCount) {
                    followersCount.textContent = data.followers_count;
                }
            } catch (error) {
                HTMLFormElement.prototype.submit.call(form);
                return;
            } finally {
                if (button) {
                    button.disabled = false;
                }
            }
        });
    });
}

function setupLikeForms() {
    document.querySelectorAll("[data-like-form]").forEach((form) => {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const button = form.querySelector("[data-like-button]");
            const icon = button ? button.querySelector("img") : null;
            const formData = new FormData(form);
            const postId = formData.get("post_id");
            const likeCount = document.querySelector(`[data-like-count="${postId}"]`);

            if (button) {
                button.disabled = true;
            }

            try {
                const response = await fetch(form.action, {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                    },
                });

                if (!response.ok) {
                    throw new Error("Like request failed");
                }

                const data = await response.json();

                if (button) {
                    button.classList.toggle("is-liked", data.liked);
                    button.setAttribute("aria-pressed", data.liked ? "true" : "false");
                    button.title = data.liked ? "Unlike this post" : "Like this post";
                }

                if (icon) {
                    icon.src = data.liked ? icon.dataset.likedSrc : icon.dataset.unlikedSrc;
                }

                if (likeCount) {
                    likeCount.textContent = data.like_text;
                    likeCount.hidden = !data.like_text;
                }
            } catch (error) {
                HTMLFormElement.prototype.submit.call(form);
                return;
            } finally {
                if (button) {
                    button.disabled = false;
                }
            }
        });
    });
}

function setupShareButtons() {
    document.querySelectorAll("[data-share-button]").forEach((button) => {
        button.addEventListener("click", async () => {
            const url = button.dataset.shareUrl || window.location.href;
            const title = document.title;

            try {
                if (navigator.share) {
                    await navigator.share({ title, url });
                } else if (navigator.clipboard) {
                    await navigator.clipboard.writeText(url);
                    button.classList.add("is-copied");
                    button.title = "Link copied";
                    window.setTimeout(() => {
                        button.classList.remove("is-copied");
                        button.title = "Copy post link";
                    }, 1600);
                }
            } catch (error) {
                button.title = "Could not share";
            }
        });
    });
}

function setupCommentToggles() {
    document.querySelectorAll("[data-comments-toggle]").forEach((button) => {
        button.addEventListener("click", () => {
            const targetId = button.dataset.commentsTarget;
            const comments = targetId ? document.getElementById(targetId) : null;

            if (!comments) {
                return;
            }

            comments.querySelectorAll("[data-extra-comment]").forEach((comment) => {
                comment.hidden = false;
            });

            comments.querySelectorAll("[data-comments-toggle]").forEach((toggle) => {
                toggle.hidden = true;
            });

            button.setAttribute("aria-expanded", "true");
            comments.scrollIntoView({ behavior: "smooth", block: "nearest" });
        });
    });
}

function setupDeleteForms() {
    document.querySelectorAll("[data-delete-form]").forEach((form) => {
        form.addEventListener("submit", (event) => {
            const message = form.dataset.confirmMessage || "Delete this post?";

            if (!window.confirm(message)) {
                event.preventDefault();
                return;
            }

            setBusy(form, true);
        });
    });
}

function setupAutoGrow() {
    document.querySelectorAll("[data-autogrow]").forEach((field) => {
        const resize = () => {
            field.style.height = "auto";
            field.style.height = `${field.scrollHeight}px`;
        };

        field.addEventListener("input", resize);
        resize();
    });
}

function setupImagePreviews() {
    document.querySelectorAll("[data-image-input]").forEach((input) => {
        const form = input.closest("form");
        const preview = form ? form.querySelector("[data-image-preview]") : null;

        if (!preview) {
            return;
        }

        input.addEventListener("change", () => {
            const file = input.files && input.files[0];

            if (!file) {
                preview.hidden = true;
                preview.removeAttribute("src");
                return;
            }

            preview.src = URL.createObjectURL(file);
            preview.hidden = false;
        });
    });
}

function setupBusyForms() {
    document.querySelectorAll("[data-busy-form]").forEach((form) => {
        form.addEventListener("submit", () => setBusy(form, true));
    });
}

document.addEventListener("DOMContentLoaded", () => {
    setupThemeToggle();
    setupFollowForms();
    setupLikeForms();
    setupShareButtons();
    setupCommentToggles();
    setupDeleteForms();
    setupAutoGrow();
    setupImagePreviews();
    setupBusyForms();
});
