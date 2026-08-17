import { useEffect, useState } from "react";
import "./App.css";

type VocabularyItem = {
  term: string;
  meaning: string;
  difficulty: string;
};

type ContentAnalysis = {
  language: string;
  difficulty: string;
  vocabulary: VocabularyItem[];
  grammar_concepts: string[];
  idioms: string[];
  slang: string[];
  cultural_notes: string[];
};

type Lesson = {
  title: string;
  learner_level: string;
  focus_concepts: string[];
  explanation: string;
  examples: string[];
  cultural_context: string;
};

type Exercise = {
  id: string;
  type: string;
  prompt: string;
  choices: string[] | null;
  target_concept: string;
};

type DemoCompareResponse = {
  content: string;
  content_analysis: ContentAnalysis;
  beginner_lesson: Lesson;
  intermediate_lesson: Lesson;
  beginner_exercises: Exercise[];
  intermediate_exercises: Exercise[];
  personalization_differences: string[];
};

type SubmitAnswerResponse = {
  profile_id: string;
  exercise_id: string;
  user_answer: string;
  correct_answer: string;
  evaluation: {
    is_correct: boolean;
    feedback: string;
    mistake_type: string;
  };
  updated_mastery: {
    concept: string;
    score_before: number;
    score_after: number;
    explanation: string;
  };
  next_recommendation: string;
};

type ConceptMasteryState = {
  profile_id: string;
  concept: string;
  score: number;
  correct_count: number;
  mistake_count: number;
  updated_at: string | null;
};

type LearnerStateResponse = {
  profile_id: string;
  mastery: ConceptMasteryState[];
};

const DEFAULT_CONTENT =
  "No sé qué tiene tu mirada, pero me hace recordar algo que nunca viví.";


function LearnerStateDashboard({
  profileId,
  title,
  refreshKey,
}: {
  profileId: string;
  title: string;
  refreshKey: number;
}) {
  const [learnerState, setLearnerState] =
    useState<LearnerStateResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    let shouldIgnore = false;

    async function loadLearnerState() {
      setIsLoading(true);

      try {
        const response = await fetch(
          `http://localhost:8000/demo/profiles/${profileId}/state`
        );

        if (!response.ok) {
          throw new Error(`Backend returned status ${response.status}`);
        }

        const data: LearnerStateResponse = await response.json();

        if (!shouldIgnore) {
          setLearnerState(data);
        }
      } catch (error) {
        console.error(error);
      } finally {
        if (!shouldIgnore) {
          setIsLoading(false);
        }
      }
    }

    loadLearnerState();

    return () => {
      shouldIgnore = true;
    };
  }, [profileId, refreshKey]);

  return (
    <section className="state-card">
      <div className="state-card-header">
        <p className="eyebrow">Learner State</p>
        <h2>{title}</h2>
      </div>

      {isLoading && <p className="muted-text">Loading learner state...</p>}

      {!isLoading && (!learnerState || learnerState.mastery.length === 0) && (
        <p className="muted-text">
          No answered exercises yet. Submit an answer to create mastery data.
        </p>
      )}

      {learnerState && learnerState.mastery.length > 0 && (
        <div className="mastery-list">
          {learnerState.mastery.map((item) => (
            <div className="mastery-row" key={item.concept}>
              <div>
                <p className="mastery-concept">{item.concept}</p>
                <p className="mastery-counts">
                  Correct: {item.correct_count} · Mistakes: {item.mistake_count}
                </p>
              </div>

              <div className="mastery-score">
                {Math.round(item.score * 100)}%
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

function LessonCard({
  title,
  learnerLabel,
  profileId,
  lesson,
  exercises,
  onAnswerSubmitted,
}: {
  title: string;
  learnerLabel: string;
  profileId: string;
  lesson: Lesson;
  exercises: Exercise[];
  onAnswerSubmitted: () => void;
}) {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [submissions, setSubmissions] = useState<
    Record<string, SubmitAnswerResponse>
  >({});
  const [loadingExerciseId, setLoadingExerciseId] = useState<string | null>(
    null
  );

  async function submitAnswer(exercise: Exercise, exerciseId: string) {
    const userAnswer = answers[exerciseId] ?? "";

    if (!userAnswer.trim()) {
      return;
    }

    setLoadingExerciseId(exerciseId);

    try {
      const response = await fetch("http://localhost:8000/demo/submit-answer", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          profile_id: profileId,
          exercise_id: exerciseId,
          user_answer: userAnswer,
        }),
      });

      if (!response.ok) {
        throw new Error(`Backend returned status ${response.status}`);
      }

      const data: SubmitAnswerResponse = await response.json();

      setSubmissions((current) => ({
        ...current,
        [exerciseId]: data,
      }));
      onAnswerSubmitted();
    } catch (error) {
      console.error(error);
      alert("Could not submit answer. Make sure the backend is running.");
    } finally {
      setLoadingExerciseId(null);
    }
  }

  return (
    <section className="lesson-card">
      <div className="lesson-card-header">
        <p className="eyebrow">{learnerLabel}</p>
        <h2>{title}</h2>
        <span className="level-pill">Level {lesson.learner_level}</span>
      </div>

      <div className="section-block">
        <h3>Focus Concepts</h3>
        <div className="tag-list">
          {lesson.focus_concepts.map((concept) => (
            <span className="tag" key={concept}>
              {concept}
            </span>
          ))}
        </div>
      </div>

      <div className="section-block">
        <h3>Explanation</h3>
        <p>{lesson.explanation}</p>
      </div>

      <div className="section-block">
        <h3>Examples</h3>
        <ul>
          {lesson.examples.map((example) => (
            <li key={example}>{example}</li>
          ))}
        </ul>
      </div>

      <div className="section-block">
        <h3>Cultural Context</h3>
        <p>{lesson.cultural_context}</p>
      </div>

      <div className="section-block">
        <h3>Exercises</h3>

        <div className="exercise-list">
          {exercises.map((exercise, index) => {
            const exerciseId = exercise.id;
            const submitted = submissions[exerciseId];

            return (
              <div className="exercise-card" key={exerciseId}>
                <p className="exercise-type">{exercise.type}</p>
                <p>{exercise.prompt}</p>

                {exercise.choices ? (
                  <div className="choice-list">
                    {exercise.choices.map((choice) => (
                      <button
                        className={
                          answers[exerciseId] === choice
                            ? "choice-button selected"
                            : "choice-button"
                        }
                        key={choice}
                        type="button"
                        onClick={() =>
                          setAnswers((current) => ({
                            ...current,
                            [exerciseId]: choice,
                          }))
                        }
                      >
                        {choice}
                      </button>
                    ))}
                  </div>
                ) : (
                  <input
                    className="answer-input"
                    value={answers[exerciseId] ?? ""}
                    onChange={(event) =>
                      setAnswers((current) => ({
                        ...current,
                        [exerciseId]: event.target.value,
                      }))
                    }
                    placeholder="Type your answer..."
                  />
                )}

                <p className="answer">
                  Target: <strong>{exercise.target_concept}</strong>
                </p>

                <button
                  className="submit-answer-button"
                  type="button"
                  disabled={
                    loadingExerciseId === exerciseId ||
                    !(answers[exerciseId] ?? "").trim()
                  }
                  onClick={() => submitAnswer(exercise, exerciseId)}
                >
                  {loadingExerciseId === exerciseId
                    ? "Checking..."
                    : "Submit Answer"}
                </button>

                {submitted && (
                  <div
                    className={
                      submitted.evaluation.is_correct
                        ? "feedback-panel correct"
                        : "feedback-panel incorrect"
                    }
                  >
                    <p className="feedback-status">
                      {submitted.evaluation.is_correct
                        ? "Correct"
                        : "Needs Review"}
                    </p>

                    <p>{submitted.evaluation.feedback}</p>

                    <div className="mastery-box">
                      <p>
                        Mistake type:{" "}
                        <strong>{submitted.evaluation.mistake_type}</strong>
                      </p>
                      <p>
                        Mastery:{" "}
                        <strong>
                          {Math.round(
                            submitted.updated_mastery.score_before * 100
                          )}
                          %
                        </strong>{" "}
                        →{" "}
                        <strong>
                          {Math.round(
                            submitted.updated_mastery.score_after * 100
                          )}
                          %
                        </strong>
                      </p>
                    </div>

                    <p className="recommendation">
                      Next: {submitted.next_recommendation}
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

function App() {
  const [content, setContent] = useState(DEFAULT_CONTENT);
  const [result, setResult] = useState<DemoCompareResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [stateRefreshKey, setStateRefreshKey] = useState(0);

  async function generateLessons() {
    setIsLoading(true);
    setErrorMessage("");

    try {
      const response = await fetch("http://localhost:8000/demo/compare", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ content }),
      });

      if (!response.ok) {
        throw new Error(`Backend returned status ${response.status}`);
      }

      const data: DemoCompareResponse = await response.json();
      setResult(data);
    } catch (error) {
      console.error(error);
      setErrorMessage(
        "Could not connect to the backend. Make sure FastAPI is running on port 8000."
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="hero">
        <p className="eyebrow">FluentVerse MVP</p>
        <h1>Same Content, Different Learning Paths</h1>
        <p className="hero-subtitle">
          Paste a Spanish lyric-style sentence and see how FluentVerse creates
          different lessons for a beginner and an intermediate learner.
        </p>
      </section>

      <section className="input-panel">
        <label htmlFor="content">Spanish content</label>
        <textarea
          id="content"
          value={content}
          onChange={(event) => setContent(event.target.value)}
          rows={4}
        />

        <button onClick={generateLessons} disabled={isLoading}>
          {isLoading ? "Generating..." : "Generate Personalized Lessons"}
        </button>

        {errorMessage && <p className="error-message">{errorMessage}</p>}
      </section>

      {result && (
        <>
          <section className="analysis-panel">
            <h2>Content Analysis</h2>
            <div className="analysis-grid">
              <div>
                <p className="analysis-label">Language</p>
                <p>{result.content_analysis.language}</p>
              </div>
              <div>
                <p className="analysis-label">Difficulty</p>
                <p>{result.content_analysis.difficulty}</p>
              </div>
              <div>
                <p className="analysis-label">Grammar</p>
                <p>{result.content_analysis.grammar_concepts.join(", ")}</p>
              </div>
            </div>
          </section>

          <section className="lesson-grid">
            <LessonCard
              title={result.beginner_lesson.title}
              learnerLabel="Beginner Learner"
              profileId="beginner_demo"
              lesson={result.beginner_lesson}
              exercises={result.beginner_exercises}
              onAnswerSubmitted={() => setStateRefreshKey((value) => value + 1)}
            />

            <LessonCard
              title={result.intermediate_lesson.title}
              learnerLabel="Intermediate Learner"
              profileId="intermediate_demo"
              lesson={result.intermediate_lesson}
              exercises={result.intermediate_exercises}
              onAnswerSubmitted={() => setStateRefreshKey((value) => value + 1)}
            />
          </section>

          <section className="state-grid">
            <LearnerStateDashboard
              profileId="beginner_demo"
              title="Beginner Learner"
              refreshKey={stateRefreshKey}
            />

            <LearnerStateDashboard
              profileId="intermediate_demo"
              title="Intermediate Learner"
              refreshKey={stateRefreshKey}
            />
          </section>

          <section className="differences-panel">
            <h2>Why These Lessons Are Different</h2>
            <ul>
              {result.personalization_differences.map((difference) => (
                <li key={difference}>{difference}</li>
              ))}
            </ul>
          </section>
        </>
      )}
    </main>
  );
}

export default App;