import { PracticeLoader } from "./PracticeLoader";

/** Next 15: route params arrive as a Promise. */
export default async function PracticeProblemPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <PracticeLoader problemId={id} />;
}
