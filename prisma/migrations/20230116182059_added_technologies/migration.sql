-- CreateTable
CREATE TABLE "Technology" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL
);

-- CreateTable
CREATE TABLE "_TechnologyToTodo" (
    "A" TEXT NOT NULL,
    "B" TEXT NOT NULL,
    CONSTRAINT "_TechnologyToTodo_A_fkey" FOREIGN KEY ("A") REFERENCES "Technology" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT "_TechnologyToTodo_B_fkey" FOREIGN KEY ("B") REFERENCES "todos" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateIndex
CREATE UNIQUE INDEX "Technology_name_key" ON "Technology"("name");

-- CreateIndex
CREATE UNIQUE INDEX "_TechnologyToTodo_AB_unique" ON "_TechnologyToTodo"("A", "B");

-- CreateIndex
CREATE INDEX "_TechnologyToTodo_B_index" ON "_TechnologyToTodo"("B");
