# パッケージごとのCI

従来の `app.yaml` の `build-app` を、次の3つのワークフローへ分離しています。すべてのpush・Pull Requestで実行します。path filterは設定していません。

| ワークフロー | チェック名 | 実行内容 |
| --- | --- | --- |
| `frontend-ci.yaml` | `Frontend checks` | frontendの型チェック・ESLint・ESLint設定ファイルのBiome検査 |
| `frontend-ci.yaml` | `Frontend tests` | StorybookのChromiumテスト・カバレッジ・JSONレポート |
| `backend-ci.yaml` | `Backend checks` | backendの型チェック・ESLint・Biome。共有の型・設定もBiomeで検査 |
| `backend-ci.yaml` | `Backend tests` | backendのBunテスト・カバレッジ |
| `schemas-ci.yaml` | `Schemas checks` | schemasの型チェック・Biome |

schemasにはテストスクリプトが定義されていないため、存在しないテストコマンドは呼び出していません。frontendのテストはStorybook連携のブラウザテストであり、`Frontend tests` ジョブでChromiumとシステム依存関係をインストールします。

## 依存関係と検証の独立性

各ジョブはNode.js 22・Bun 1.3.13を準備し、workspaceルートの `app` で `bun install --frozen-lockfile` を実行します。別ジョブの `node_modules` に依存せず、単独で再実行できます。

frontend・backendのテストジョブは静的チェックの成否に依存しません。静的チェック内でも、依存関係のインストールが成功していれば、型チェックが失敗した場合も後続のLintを実行します。先行する検証の失敗は、ジョブの失敗として維持されます。

## テスト結果

frontendは `app/frontend/coverage/`、backendは `app/backend/coverage/` をartifactとして保存します。frontendには `coverage/test-result.json` も出力し、Actionsのジョブサマリーへ件数を表示します。テスト結果が出力されない場合や、テスト件数が0の場合は結果報告を失敗させます。

参照元と同様に、同じリポジトリのPull Requestにはfrontendのテスト結果をコメントします。fork・DependabotからのPull Requestではコメントせず、artifactとサマリーを利用します。テスト実行時に検証対象のコードを扱うため、`pull_request_target` は使用していません。

参照元: [wait-time-calculationのFrontend CI](https://github.com/kishimin/wait-time-calculation/blob/ab0f440e5abf9f60e5152fba12fb7e5d8e5893a5/.github/workflows/frontend-ci.yaml)。インストール方法・パス・レポート生成は、このリポジトリのBun workspaceと既存のスクリプトに合わせています。

## 現時点の検証範囲

ローカルでは、actionlintによるワークフロー検査、workspaceの固定ロックインストール、CIと同じfrontend・backendのテストコマンドとカバレッジ出力を確認しています。frontendの結果報告処理はGitHubへの書き込みをモックし、push・通常PR・fork・Dependabot・結果欠落・テスト0件・失敗テスト・削除済みforkを検証しています。

YAMLの整形には、workspaceルートの `app` で次のコマンドを実行します。対象は `.github/workflows/` 内の `.yml`・`.yaml` です。

| 用途 | コマンド |
| --- | --- |
| 整形を適用 | `bun run format:yaml` |
| 整形状態を検査 | `bun run format:yaml:check` |

Prettierのバージョンは `app/package.json` と `app/bun.lock` で固定しています。`Backend checks` でも `format:yaml:check` を実行します。構文・式はactionlint、空白エラーは `git diff --check` で確認しています。CI設定は `non-adr-config-fix` と `critical-review` の手順でも確認しています。

既存ソースにはfrontendの型エラーとLint違反、backendのLint違反、Windows作業ツリーのCRLFに起因するBiomeの整形エラーがあります。検査を通すためのルール緩和や対象ソースの変更は行っていません。

GitHub Actions上の実行成功は、ローカル検証では保証できません。Ubuntu上でのChromiumのシステム依存関係インストールも、ローカルのWindows環境では検証していません。ワークフローはESLint設定・package.json・`app/bun.lock` と合わせて反映する必要があります。
