import { PracticeLoader } from "./PracticeLoader";

/** Next 15: route params and searchParams arrive as Promises. */
export default async function PracticeProblemPage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams?: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const { id } = await params;
  const sp = searchParams ? await searchParams : undefined;
  const rawDay = sp?.day;
  const dayNumber = typeof rawDay === "string" && !isNaN(parseInt(rawDay, 10))
    ? parseInt(rawDay, 10)
    : undefined;

  return <PracticeLoader problemId={id} dayNumber={dayNumber} />;
}

